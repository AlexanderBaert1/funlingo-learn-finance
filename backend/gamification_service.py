from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from models import (
    Achievement, UserAchievement, AchievementType, LeaderboardEntry, 
    LeaderboardType, Streak, UserProfile, UserActivity
)
import uuid

class GamificationService:
    """Service for managing gamification features like achievements, leaderboards, and streaks"""
    
    def __init__(self, db):
        self.db = db
        self.achievements_collection = db.achievements
        self.user_achievements_collection = db.user_achievements
        self.leaderboards_collection = db.leaderboards
        self.streaks_collection = db.streaks
        self.user_profiles_collection = db.user_profiles
        self.user_activities_collection = db.user_activities
    
    async def initialize_default_achievements(self):
        """Initialize default achievement set"""
        default_achievements = [
            # Streak Achievements
            {
                "name": "Getting Started",
                "description": "Complete your first lesson",
                "icon": "🌟",
                "type": AchievementType.LESSONS,
                "requirement": {"lessons_completed": 1},
                "reward_xp": 50,
                "reward_gems": 10,
                "rarity": "common"
            },
            {
                "name": "Week Warrior", 
                "description": "Maintain a 7-day learning streak",
                "icon": "🔥",
                "type": AchievementType.STREAK,
                "requirement": {"streak_days": 7},
                "reward_xp": 200,
                "reward_gems": 50,
                "rarity": "rare"
            },
            {
                "name": "Month Master",
                "description": "Maintain a 30-day learning streak", 
                "icon": "🏆",
                "type": AchievementType.STREAK,
                "requirement": {"streak_days": 30},
                "reward_xp": 1000,
                "reward_gems": 200,
                "rarity": "epic"
            },
            # XP Achievements
            {
                "name": "Knowledge Seeker",
                "description": "Earn 500 total XP",
                "icon": "🧠",
                "type": AchievementType.XP,
                "requirement": {"total_xp": 500},
                "reward_xp": 100,
                "reward_gems": 25,
                "rarity": "common"
            },
            {
                "name": "Wisdom Collector",
                "description": "Earn 2,500 total XP", 
                "icon": "📚",
                "type": AchievementType.XP,
                "requirement": {"total_xp": 2500},
                "reward_xp": 300,
                "reward_gems": 75,
                "rarity": "rare"
            },
            {
                "name": "Finance Guru",
                "description": "Earn 10,000 total XP",
                "icon": "💎",
                "type": AchievementType.XP,
                "requirement": {"total_xp": 10000},
                "reward_xp": 1000,
                "reward_gems": 300,
                "rarity": "legendary"
            },
            # Topic Achievements  
            {
                "name": "Basic Foundations",
                "description": "Complete the Finance Basics topic",
                "icon": "🏗️",
                "type": AchievementType.TOPICS,
                "requirement": {"topics_completed": ["basics"]},
                "reward_xp": 300,
                "reward_gems": 50,
                "rarity": "common"
            },
            {
                "name": "Budget Boss",
                "description": "Complete the Budgeting topic",
                "icon": "💰",
                "type": AchievementType.TOPICS,
                "requirement": {"topics_completed": ["budgeting"]},
                "reward_xp": 400,
                "reward_gems": 75,
                "rarity": "rare"
            },
            {
                "name": "Investment Wizard",
                "description": "Complete the Investing topic",
                "icon": "📈",
                "type": AchievementType.TOPICS,
                "requirement": {"topics_completed": ["investing"]},
                "reward_xp": 600,
                "reward_gems": 100,
                "rarity": "epic"
            },
            # Community Achievements
            {
                "name": "Helpful Helper", 
                "description": "Help 10 people in community discussions",
                "icon": "🤝",
                "type": AchievementType.COMMUNITY,
                "requirement": {"helpful_replies": 10},
                "reward_xp": 250,
                "reward_gems": 50,
                "rarity": "rare"
            },
            {
                "name": "Discussion Leader",
                "description": "Start 5 community discussions",
                "icon": "💬",
                "type": AchievementType.COMMUNITY,
                "requirement": {"discussions_started": 5},
                "reward_xp": 300,
                "reward_gems": 60,
                "rarity": "rare"
            },
            # Special Achievements
            {
                "name": "Perfect Score",
                "description": "Get 100% on any lesson", 
                "icon": "⭐",
                "type": AchievementType.SPECIAL,
                "requirement": {"perfect_lesson": True},
                "reward_xp": 150,
                "reward_gems": 30,
                "rarity": "rare"
            },
            {
                "name": "Challenge Champion",
                "description": "Win your first peer challenge",
                "icon": "🥇",
                "type": AchievementType.SPECIAL,
                "requirement": {"challenges_won": 1},
                "reward_xp": 500,
                "reward_gems": 100,
                "rarity": "epic"
            }
        ]
        
        for achievement_data in default_achievements:
            achievement = Achievement(**achievement_data, id=str(uuid.uuid4()))
            await self.achievements_collection.insert_one(achievement.dict())
    
    async def check_and_award_achievements(self, user_id: str, activity_data: Dict[str, Any]):
        """Check if user has earned any new achievements"""
        user_profile = await self.user_profiles_collection.find_one({"id": user_id})
        if not user_profile:
            return []
        
        all_achievements = await self.achievements_collection.find({"is_active": True}).to_list(None)
        user_achievements = await self.user_achievements_collection.find({"user_id": user_id}).to_list(None)
        earned_achievement_ids = {ua["achievement_id"] for ua in user_achievements}
        
        new_achievements = []
        
        for achievement in all_achievements:
            if achievement["id"] in earned_achievement_ids:
                continue
                
            if await self._check_achievement_requirement(user_profile, achievement, activity_data):
                # Award achievement
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement["id"],
                    progress=1.0
                )
                await self.user_achievements_collection.insert_one(user_achievement.dict())
                
                # Update user profile with rewards
                await self.user_profiles_collection.update_one(
                    {"id": user_id},
                    {
                        "$inc": {
                            "total_xp": achievement.get("reward_xp", 0),
                            "total_gems": achievement.get("reward_gems", 0)
                        },
                        "$push": {"achievements": achievement["id"]}
                    }
                )
                
                new_achievements.append(achievement)
        
        return new_achievements
    
    async def _check_achievement_requirement(self, user_profile: Dict, achievement: Dict, activity_data: Dict) -> bool:
        """Check if user meets achievement requirements"""
        requirement = achievement["requirement"]
        
        if achievement["type"] == AchievementType.STREAK:
            return user_profile.get("current_streak", 0) >= requirement.get("streak_days", 0)
        
        elif achievement["type"] == AchievementType.LESSONS:
            return len(user_profile.get("lessons_completed", [])) >= requirement.get("lessons_completed", 0)
        
        elif achievement["type"] == AchievementType.XP:
            return user_profile.get("total_xp", 0) >= requirement.get("total_xp", 0)
        
        elif achievement["type"] == AchievementType.TOPICS:
            required_topics = requirement.get("topics_completed", [])
            user_topics = set(user_profile.get("topics_completed", []))
            return all(topic in user_topics for topic in required_topics)
        
        elif achievement["type"] == AchievementType.COMMUNITY:
            # Check community-specific requirements
            if "helpful_replies" in requirement:
                # Would need to track this in user activity
                return activity_data.get("helpful_replies_total", 0) >= requirement["helpful_replies"]
            if "discussions_started" in requirement:
                return activity_data.get("discussions_started_total", 0) >= requirement["discussions_started"]
        
        elif achievement["type"] == AchievementType.SPECIAL:
            if "perfect_lesson" in requirement:
                return activity_data.get("lesson_score", 0) == 100
            if "challenges_won" in requirement:
                return activity_data.get("challenges_won_total", 0) >= requirement["challenges_won"]
        
        return False
    
    async def update_streak(self, user_id: str) -> Dict[str, Any]:
        """Update user's learning streak"""
        today = datetime.utcnow().date()
        
        # Get current streak record
        streak_record = await self.streaks_collection.find_one({"user_id": user_id})
        
        if not streak_record:
            # Create new streak record
            streak = Streak(
                user_id=user_id,
                current_streak=1,
                longest_streak=1,
                last_activity_date=datetime.utcnow()
            )
            await self.streaks_collection.insert_one(streak.dict())
            streak_record = streak.dict()
        else:
            last_activity = streak_record["last_activity_date"].date()
            
            if last_activity == today:
                # Already counted today
                return streak_record
            elif last_activity == today - timedelta(days=1):
                # Consecutive day - extend streak
                new_streak = streak_record["current_streak"] + 1
                longest_streak = max(streak_record["longest_streak"], new_streak)
                
                await self.streaks_collection.update_one(
                    {"user_id": user_id},
                    {
                        "$set": {
                            "current_streak": new_streak,
                            "longest_streak": longest_streak,
                            "last_activity_date": datetime.utcnow()
                        }
                    }
                )
                streak_record["current_streak"] = new_streak
                streak_record["longest_streak"] = longest_streak
            else:
                # Streak broken - reset
                await self.streaks_collection.update_one(
                    {"user_id": user_id},
                    {
                        "$set": {
                            "current_streak": 1,
                            "last_activity_date": datetime.utcnow()
                        }
                    }
                )
                streak_record["current_streak"] = 1
        
        # Update user profile
        await self.user_profiles_collection.update_one(
            {"id": user_id},
            {
                "$set": {
                    "current_streak": streak_record["current_streak"],
                    "longest_streak": streak_record["longest_streak"]
                }
            }
        )
        
        return streak_record
    
    async def generate_leaderboard(self, leaderboard_type: LeaderboardType, 
                                 topic_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Generate leaderboard for different categories"""
        
        now = datetime.utcnow()
        
        if leaderboard_type == LeaderboardType.WEEKLY:
            start_date = now - timedelta(days=7)
        elif leaderboard_type == LeaderboardType.MONTHLY:
            start_date = now - timedelta(days=30)
        else:
            start_date = datetime.min
        
        # Aggregate user scores based on leaderboard type
        pipeline = []
        
        if leaderboard_type == LeaderboardType.GLOBAL:
            # Global XP leaderboard
            pipeline = [
                {"$sort": {"total_xp": -1}},
                {"$limit": limit},
                {"$project": {
                    "user_id": "$id",
                    "username": 1,
                    "display_name": 1,
                    "avatar_url": 1,
                    "score": "$total_xp"
                }}
            ]
        
        elif leaderboard_type in [LeaderboardType.WEEKLY, LeaderboardType.MONTHLY]:
            # Time-based XP leaderboard
            pipeline = [
                {
                    "$match": {
                        "created_at": {"$gte": start_date}
                    }
                },
                {
                    "$group": {
                        "_id": "$user_id",
                        "score": {"$sum": "$xp_earned"}
                    }
                },
                {"$sort": {"score": -1}},
                {"$limit": limit},
                {
                    "$lookup": {
                        "from": "user_profiles",
                        "localField": "_id", 
                        "foreignField": "id",
                        "as": "profile"
                    }
                },
                {"$unwind": "$profile"},
                {"$project": {
                    "user_id": "$_id",
                    "username": "$profile.username",
                    "display_name": "$profile.display_name",
                    "avatar_url": "$profile.avatar_url",
                    "score": 1
                }}
            ]
        
        # Execute pipeline on appropriate collection
        if leaderboard_type == LeaderboardType.GLOBAL:
            results = await self.user_profiles_collection.aggregate(pipeline).to_list(None)
        else:
            results = await self.user_activities_collection.aggregate(pipeline).to_list(None)
        
        # Add ranks and create leaderboard entries
        leaderboard_entries = []
        for i, result in enumerate(results):
            entry = LeaderboardEntry(
                user_id=result["user_id"],
                username=result["username"],
                display_name=result.get("display_name"),
                avatar_url=result.get("avatar_url"),
                score=result["score"],
                rank=i + 1,
                leaderboard_type=leaderboard_type,
                period_start=start_date,
                period_end=now,
                topic_id=topic_id
            )
            leaderboard_entries.append(entry.dict())
        
        return leaderboard_entries
    
    async def record_user_activity(self, user_id: str, activity_type: str, 
                                 content_id: str = None, xp_earned: int = 0, 
                                 gems_earned: int = 0, metadata: Dict[str, Any] = None):
        """Record user activity for analytics and gamification"""
        
        activity = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            content_id=content_id,
            xp_earned=xp_earned,
            gems_earned=gems_earned,
            metadata=metadata or {}
        )
        
        await self.user_activities_collection.insert_one(activity.dict())
        
        # Update user profile totals
        await self.user_profiles_collection.update_one(
            {"id": user_id},
            {
                "$inc": {
                    "total_xp": xp_earned,
                    "total_gems": gems_earned
                },
                "$set": {
                    "last_activity": datetime.utcnow()
                }
            }
        )
    
    async def get_user_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all achievements earned by user"""
        user_achievements = await self.user_achievements_collection.find({"user_id": user_id}).to_list(None)
        achievement_ids = [ua["achievement_id"] for ua in user_achievements]
        
        achievements = await self.achievements_collection.find(
            {"id": {"$in": achievement_ids}}
        ).to_list(None)
        
        # Combine achievement data with user progress
        result = []
        for achievement in achievements:
            user_achievement = next((ua for ua in user_achievements if ua["achievement_id"] == achievement["id"]), None)
            if user_achievement:
                achievement["earned_at"] = user_achievement["earned_at"]
                achievement["progress"] = user_achievement["progress"]
                result.append(achievement)
        
        return result
    
    async def get_available_achievements(self, user_id: str) -> List[Dict[str, Any]]:
        """Get achievements user hasn't earned yet"""
        user_achievements = await self.user_achievements_collection.find({"user_id": user_id}).to_list(None)
        earned_ids = {ua["achievement_id"] for ua in user_achievements}
        
        available_achievements = await self.achievements_collection.find({
            "id": {"$nin": list(earned_ids)},
            "is_active": True
        }).to_list(None)
        
        return available_achievements