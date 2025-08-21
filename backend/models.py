from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from enum import Enum

# Base Models
class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Enums
class AchievementType(str, Enum):
    STREAK = "streak"
    LESSONS = "lessons"
    XP = "xp"
    TOPICS = "topics"
    COMMUNITY = "community"
    SPECIAL = "special"

class LeaderboardType(str, Enum):
    GLOBAL = "global"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    TOPIC = "topic"
    FRIENDS = "friends"

class ChallengeType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    PEER = "peer"
    TOPIC_MASTERY = "topic_mastery"

class DiscussionType(str, Enum):
    GENERAL = "general"
    TOPIC_SPECIFIC = "topic_specific"
    LESSON_HELP = "lesson_help"
    CHALLENGE = "challenge"

class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple-choice"
    FILL_BLANK = "fill-blank"
    TRUE_FALSE = "true-false"
    SCENARIO = "scenario"
    CALCULATION = "calculation"

# User Profile Models
class UserProfile(TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    current_streak: int = 0
    longest_streak: int = 0
    total_xp: int = 0
    total_gems: int = 0
    hearts: int = 3
    max_hearts: int = 5
    last_heart_refill: datetime = Field(default_factory=datetime.utcnow)
    level: int = 1
    topics_completed: List[str] = []
    lessons_completed: List[str] = []
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    preferences: Dict[str, Any] = {}
    achievements: List[str] = []
    is_premium: bool = False

class UserProfileCreate(BaseModel):
    username: str
    email: str
    display_name: Optional[str] = None

class UserProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

# Gamification Models
class Achievement(TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    icon: str
    badge_url: Optional[str] = None
    type: AchievementType
    requirement: Dict[str, Any]  # e.g., {"streak_days": 7} or {"lessons_completed": 10}
    reward_xp: int = 0
    reward_gems: int = 0
    is_active: bool = True
    rarity: str = "common"  # common, rare, epic, legendary

class UserAchievement(TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    achievement_id: str
    earned_at: datetime = Field(default_factory=datetime.utcnow)
    progress: float = 0.0  # For achievements that have progress tracking

class LeaderboardEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    username: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    score: int
    rank: int
    leaderboard_type: LeaderboardType
    period_start: datetime
    period_end: datetime
    topic_id: Optional[str] = None  # For topic-specific leaderboards

class Streak(TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    current_streak: int = 0
    longest_streak: int = 0
    last_activity_date: datetime = Field(default_factory=datetime.utcnow)
    streak_freeze_count: int = 0  # Premium feature
    total_freeze_used: int = 0

# Enhanced Educational Content Models
class Question(TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    lesson_id: str
    topic_id: str
    question: str
    type: QuestionType
    options: Optional[List[str]] = None  # For multiple choice
    correct_answer: str
    explanation: str
    difficulty: int = 1  # 1-5 scale
    xp_reward: int = 10
    hints: List[str] = []
    tags: List[str] = []
    is_ai_generated: bool = False
    scenario_context: Optional[str] = None  # For scenario-based questions
    
class Lesson(TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic_id: str
    title: str
    description: str
    content: Optional[str] = None
    duration: int  # in minutes
    xp_reward: int
    order: int
    prerequisites: List[str] = []  # lesson IDs
    difficulty: int = 1
    is_locked: bool = False
    lesson_type: str = "standard"  # standard, practice, review, challenge
    objectives: List[str] = []

class Topic(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    icon: str
    color: str
    order: int
    total_lessons: int
    estimated_time: int  # total minutes
    difficulty: int = 1
    prerequisites: List[str] = []  # topic IDs
    is_locked: bool = False
    category: str = "finance"

# AI-Powered Features Models
class LearningPath(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    description: str
    recommended_lessons: List[Dict[str, Any]]  # lesson info with priority
    difficulty_adjustment: float = 1.0
    estimated_completion: int  # days
    is_active: bool = True
    progress: float = 0.0

class AIRecommendation(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    type: str  # lesson, topic, practice, review
    content_id: str
    reason: str
    confidence_score: float
    priority: int = 1
    is_viewed: bool = False
    is_accepted: bool = False

class AIGeneratedQuestion(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    topic_id: str
    lesson_id: Optional[str] = None
    prompt_used: str
    generated_question: Dict[str, Any]
    difficulty: int
    is_approved: bool = False
    feedback_score: Optional[float] = None

# Community Features Models
class Discussion(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    author_id: str
    author_username: str
    topic_id: Optional[str] = None
    lesson_id: Optional[str] = None
    discussion_type: DiscussionType
    tags: List[str] = []
    upvotes: int = 0
    downvotes: int = 0
    reply_count: int = 0
    is_pinned: bool = False
    is_resolved: bool = False

class DiscussionReply(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    discussion_id: str
    content: str
    author_id: str
    author_username: str
    parent_reply_id: Optional[str] = None  # For nested replies
    upvotes: int = 0
    downvotes: int = 0
    is_solution: bool = False

class Challenge(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    challenge_type: ChallengeType
    creator_id: str
    topic_id: Optional[str] = None
    participants: List[str] = []
    max_participants: int = 100
    start_date: datetime
    end_date: datetime
    rules: Dict[str, Any] = {}
    prizes: Dict[str, Any] = {}
    is_active: bool = True
    difficulty: int = 1

class ChallengeParticipant(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    challenge_id: str
    user_id: str
    username: str
    score: int = 0
    rank: Optional[int] = None
    progress: Dict[str, Any] = {}
    completed_at: Optional[datetime] = None
    is_winner: bool = False

class StudyGroup(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    creator_id: str
    members: List[str] = []
    max_members: int = 20
    topic_focus: List[str] = []  # topic IDs
    is_public: bool = True
    invitation_code: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    activity_feed: List[Dict[str, Any]] = []

# Progress and Analytics Models
class UserProgress(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    lesson_id: str
    topic_id: str
    status: str = "not_started"  # not_started, in_progress, completed, mastered
    progress_percentage: float = 0.0
    score: Optional[int] = None
    time_spent: int = 0  # seconds
    attempts: int = 0
    mastery_level: float = 0.0
    last_accessed: datetime = Field(default_factory=datetime.utcnow)

class UserActivity(BaseModel, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    activity_type: str  # lesson_completed, achievement_earned, streak_extended, etc.
    content_id: Optional[str] = None
    xp_earned: int = 0
    gems_earned: int = 0
    metadata: Dict[str, Any] = {}

# Request/Response Models
class QuestionResponse(BaseModel):
    question_id: str
    user_answer: str
    is_correct: bool
    time_taken: int  # seconds

class LessonCompletionRequest(BaseModel):
    lesson_id: str
    topic_id: str
    question_responses: List[QuestionResponse]
    total_time: int  # seconds

class AIQuestionRequest(BaseModel):
    topic_id: str
    lesson_id: Optional[str] = None
    difficulty: int = 1
    question_type: QuestionType = QuestionType.MULTIPLE_CHOICE
    context: Optional[str] = None