from fastapi import FastAPI, APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

# Import all models
from models import *
from ai_service import AIService
from gamification_service import GamificationService
from community_service import CommunityService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize services
ai_service = AIService()
gamification_service = GamificationService(db)
community_service = CommunityService(db)

# Create the main app
app = FastAPI(title="Finlingo Enhanced API", version="2.0.0")

# Create API router
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# ==================== USER PROFILE ENDPOINTS ====================

@api_router.post("/users", response_model=UserProfile)
async def create_user_profile(user_data: UserProfileCreate):
    """Create a new user profile"""
    # Check if user already exists
    existing_user = await db.user_profiles.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_profile = UserProfile(**user_data.dict())
    await db.user_profiles.insert_one(user_profile.dict())
    
    # Initialize default achievements
    await gamification_service.initialize_default_achievements()
    
    return user_profile

@api_router.get("/users/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: str):
    """Get user profile by ID"""
    user = await db.user_profiles.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(**user)

@api_router.put("/users/{user_id}", response_model=UserProfile)
async def update_user_profile(user_id: str, update_data: UserProfileUpdate):
    """Update user profile"""
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await db.user_profiles.update_one(
        {"id": user_id},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = await db.user_profiles.find_one({"id": user_id})
    return UserProfile(**updated_user)

# ==================== ENHANCED EDUCATIONAL CONTENT ENDPOINTS ====================

@api_router.get("/topics", response_model=List[Topic])
async def get_all_topics():
    """Get all available topics"""
    topics = await db.topics.find().to_list(1000)
    return [Topic(**topic) for topic in topics]

@api_router.get("/topics/{topic_id}/lessons", response_model=List[Lesson])
async def get_topic_lessons(topic_id: str):
    """Get all lessons for a topic"""
    lessons = await db.lessons.find({"topic_id": topic_id}).sort("order", 1).to_list(1000)
    return [Lesson(**lesson) for lesson in lessons]

@api_router.get("/lessons/{lesson_id}/questions", response_model=List[Question])
async def get_lesson_questions(lesson_id: str):
    """Get questions for a lesson"""
    questions = await db.questions.find({"lesson_id": lesson_id}).to_list(1000)
    return [Question(**question) for question in questions]

@api_router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(lesson_id: str, completion_data: LessonCompletionRequest):
    """Complete a lesson and update user progress"""
    
    # Calculate score and XP
    total_questions = len(completion_data.question_responses)
    correct_answers = sum(1 for resp in completion_data.question_responses if resp.is_correct)
    score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Get lesson info for XP calculation
    lesson = await db.lessons.find_one({"id": lesson_id})
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    base_xp = lesson.get("xp_reward", 100)
    xp_earned = int(base_xp * (score_percentage / 100))
    
    # Update user progress
    user_progress = UserProgress(
        user_id=completion_data.user_id if hasattr(completion_data, 'user_id') else "default_user",
        lesson_id=lesson_id,
        topic_id=completion_data.topic_id,
        status="completed",
        progress_percentage=100.0,
        score=int(score_percentage),
        time_spent=completion_data.total_time,
        attempts=1
    )
    
    await db.user_progress.insert_one(user_progress.dict())
    
    # Update user profile
    user_id = completion_data.user_id if hasattr(completion_data, 'user_id') else "default_user"
    await db.user_profiles.update_one(
        {"id": user_id},
        {
            "$addToSet": {"lessons_completed": lesson_id},
            "$inc": {"total_xp": xp_earned, "total_gems": xp_earned // 10}
        }
    )
    
    # Update streak
    await gamification_service.update_streak(user_id)
    
    # Record activity
    await gamification_service.record_user_activity(
        user_id=user_id,
        activity_type="lesson_completed",
        content_id=lesson_id,
        xp_earned=xp_earned,
        gems_earned=xp_earned // 10,
        metadata={"score": score_percentage, "time_spent": completion_data.total_time}
    )
    
    # Check for new achievements
    activity_data = {"lesson_score": score_percentage}
    new_achievements = await gamification_service.check_and_award_achievements(user_id, activity_data)
    
    return {
        "score": score_percentage,
        "xp_earned": xp_earned,
        "gems_earned": xp_earned // 10,
        "new_achievements": new_achievements
    }

# ==================== AI-POWERED FEATURES ENDPOINTS ====================

@api_router.post("/ai/generate-questions")
async def generate_ai_questions(request: AIQuestionRequest):
    """Generate AI-powered questions"""
    try:
        questions = await ai_service.generate_questions(
            topic_id=request.topic_id,
            lesson_id=request.lesson_id or "general",
            difficulty=request.difficulty,
            question_type=request.question_type,
            count=5,
            context=request.context
        )
        
        # Save generated questions to database
        for question_data in questions:
            question = Question(**question_data)
            await db.questions.insert_one(question.dict())
        
        return {"questions": questions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")

@api_router.get("/ai/recommendations/{user_id}")
async def get_personalized_recommendations(user_id: str):
    """Get AI-powered personalized learning recommendations"""
    try:
        # Get user progress and history
        user_profile = await db.user_profiles.find_one({"id": user_id})
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        learning_history = await db.user_activities.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(20).to_list(None)
        
        recommendations = await ai_service.generate_personalized_recommendations(
            user_id=user_id,
            user_progress=user_profile,
            learning_history=learning_history
        )
        
        # Save recommendations
        for rec_data in recommendations:
            rec = AIRecommendation(**rec_data)
            await db.ai_recommendations.insert_one(rec.dict())
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@api_router.post("/ai/learning-path/{user_id}")
async def create_learning_path(user_id: str, goals: List[str], available_time: int = 30):
    """Create a personalized learning path"""
    try:
        user_profile = await db.user_profiles.find_one({"id": user_id})
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        learning_path = await ai_service.generate_learning_path(
            user_id=user_id,
            goals=goals,
            current_level=user_profile.get("level", 1),
            available_time=available_time
        )
        
        # Save learning path
        if learning_path:
            path = LearningPath(**learning_path)
            await db.learning_paths.insert_one(path.dict())
        
        return {"learning_path": learning_path}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating learning path: {str(e)}")

# ==================== GAMIFICATION ENDPOINTS ====================

@api_router.get("/achievements")
async def get_all_achievements():
    """Get all available achievements"""
    achievements = await db.achievements.find({"is_active": True}).to_list(None)
    return achievements

@api_router.get("/users/{user_id}/achievements")
async def get_user_achievements(user_id: str):
    """Get user's earned achievements"""
    achievements = await gamification_service.get_user_achievements(user_id)
    return achievements

@api_router.get("/users/{user_id}/achievements/available")
async def get_available_achievements(user_id: str):
    """Get achievements user can still earn"""
    achievements = await gamification_service.get_available_achievements(user_id)
    return achievements

@api_router.get("/leaderboard/{leaderboard_type}")
async def get_leaderboard(leaderboard_type: LeaderboardType, topic_id: Optional[str] = None, limit: int = 50):
    """Get leaderboard data"""
    leaderboard = await gamification_service.generate_leaderboard(leaderboard_type, topic_id, limit)
    return {"leaderboard": leaderboard, "type": leaderboard_type}

@api_router.get("/users/{user_id}/streak")
async def get_user_streak(user_id: str):
    """Get user's current streak information"""
    streak = await db.streaks.find_one({"user_id": user_id})
    if not streak:
        return {"current_streak": 0, "longest_streak": 0}
    return streak

@api_router.post("/users/{user_id}/streak/update")
async def update_user_streak(user_id: str):
    """Update user's streak (called when user completes daily activity)"""
    streak = await gamification_service.update_streak(user_id)
    return streak

# ==================== COMMUNITY FEATURES ENDPOINTS ====================

@api_router.post("/discussions")
async def create_discussion(
    title: str,
    content: str,
    author_id: str,
    discussion_type: DiscussionType,
    topic_id: Optional[str] = None,
    lesson_id: Optional[str] = None,
    tags: Optional[List[str]] = None
):
    """Create a new discussion"""
    discussion = await community_service.create_discussion(
        title=title,
        content=content,
        author_id=author_id,
        discussion_type=discussion_type,
        topic_id=topic_id,
        lesson_id=lesson_id,
        tags=tags or []
    )
    return discussion

@api_router.get("/discussions")
async def get_discussions(
    discussion_type: Optional[DiscussionType] = None,
    topic_id: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "created_at"
):
    """Get discussions with filtering"""
    discussions = await community_service.get_discussions(
        discussion_type=discussion_type,
        topic_id=topic_id,
        limit=limit,
        offset=offset,
        sort_by=sort_by
    )
    return discussions

@api_router.post("/discussions/{discussion_id}/replies")
async def add_discussion_reply(
    discussion_id: str,
    content: str,
    author_id: str,
    parent_reply_id: Optional[str] = None
):
    """Add a reply to a discussion"""
    reply = await community_service.add_discussion_reply(
        discussion_id=discussion_id,
        content=content,
        author_id=author_id,
        parent_reply_id=parent_reply_id
    )
    return reply

@api_router.post("/discussions/{discussion_id}/vote")
async def vote_on_discussion(discussion_id: str, user_id: str, vote_type: str):
    """Vote on a discussion"""
    discussion = await community_service.vote_discussion(discussion_id, user_id, vote_type)
    return discussion

@api_router.post("/challenges")
async def create_challenge(
    title: str,
    description: str,
    creator_id: str,
    challenge_type: ChallengeType,
    topic_id: Optional[str] = None,
    duration_days: int = 7,
    max_participants: int = 100
):
    """Create a new challenge"""
    challenge = await community_service.create_challenge(
        title=title,
        description=description,
        creator_id=creator_id,
        challenge_type=challenge_type,
        topic_id=topic_id,
        duration_days=duration_days,
        max_participants=max_participants
    )
    return challenge

@api_router.get("/challenges")
async def get_active_challenges(
    user_id: Optional[str] = None,
    challenge_type: Optional[ChallengeType] = None,
    limit: int = 20
):
    """Get active challenges"""
    challenges = await community_service.get_active_challenges(
        user_id=user_id,
        challenge_type=challenge_type,
        limit=limit
    )
    return challenges

@api_router.post("/challenges/{challenge_id}/join")
async def join_challenge(challenge_id: str, user_id: str):
    """Join a challenge"""
    participant = await community_service.join_challenge(challenge_id, user_id)
    return participant

@api_router.post("/study-groups")
async def create_study_group(
    name: str,
    description: str,
    creator_id: str,
    topic_focus: Optional[List[str]] = None,
    max_members: int = 20,
    is_public: bool = True
):
    """Create a new study group"""
    study_group = await community_service.create_study_group(
        name=name,
        description=description,
        creator_id=creator_id,
        topic_focus=topic_focus or [],
        max_members=max_members,
        is_public=is_public
    )
    return study_group

@api_router.get("/study-groups/search")
async def search_study_groups(
    query: str = "",
    topic_filter: Optional[List[str]] = None,
    public_only: bool = True,
    limit: int = 20
):
    """Search for study groups"""
    groups = await community_service.search_study_groups(
        query=query,
        topic_filter=topic_filter or [],
        public_only=public_only,
        limit=limit
    )
    return groups

@api_router.post("/study-groups/{group_id}/join")
async def join_study_group(group_id: str, user_id: str, invitation_code: Optional[str] = None):
    """Join a study group"""
    result = await community_service.join_study_group(group_id, user_id, invitation_code)
    return result

# ==================== ANALYTICS ENDPOINTS ====================

@api_router.get("/users/{user_id}/progress")
async def get_user_progress(user_id: str):
    """Get detailed user progress analytics"""
    
    # Get overall progress
    user_profile = await db.user_profiles.find_one({"id": user_id})
    if not user_profile:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get lesson progress
    lesson_progress = await db.user_progress.find({"user_id": user_id}).to_list(None)
    
    # Get recent activities
    recent_activities = await db.user_activities.find(
        {"user_id": user_id}
    ).sort("created_at", -1).limit(10).to_list(None)
    
    # Calculate statistics
    total_lessons_completed = len(user_profile.get("lessons_completed", []))
    total_topics_completed = len(user_profile.get("topics_completed", []))
    
    return {
        "profile": user_profile,
        "lesson_progress": lesson_progress,
        "recent_activities": recent_activities,
        "statistics": {
            "total_lessons_completed": total_lessons_completed,
            "total_topics_completed": total_topics_completed,
            "total_xp": user_profile.get("total_xp", 0),
            "current_streak": user_profile.get("current_streak", 0),
            "longest_streak": user_profile.get("longest_streak", 0)
        }
    }

# Include the router in the main app
app.include_router(api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()