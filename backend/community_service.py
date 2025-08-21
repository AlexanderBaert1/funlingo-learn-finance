from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from models import (
    Discussion, DiscussionReply, Challenge, ChallengeParticipant, 
    StudyGroup, DiscussionType, ChallengeType
)
import uuid

class CommunityService:
    """Service for managing community features like discussions, challenges, and study groups"""
    
    def __init__(self, db):
        self.db = db
        self.discussions_collection = db.discussions
        self.discussion_replies_collection = db.discussion_replies
        self.challenges_collection = db.challenges
        self.challenge_participants_collection = db.challenge_participants
        self.study_groups_collection = db.study_groups
        self.user_profiles_collection = db.user_profiles
    
    async def create_discussion(self, title: str, content: str, author_id: str,
                              discussion_type: DiscussionType, topic_id: Optional[str] = None,
                              lesson_id: Optional[str] = None, tags: List[str] = None) -> Dict[str, Any]:
        """Create a new community discussion"""
        
        # Get author info
        author = await self.user_profiles_collection.find_one({"id": author_id})
        if not author:
            raise ValueError("Author not found")
        
        discussion = Discussion(
            title=title,
            content=content,
            author_id=author_id,
            author_username=author["username"],
            topic_id=topic_id,
            lesson_id=lesson_id,
            discussion_type=discussion_type,
            tags=tags or []
        )
        
        result = await self.discussions_collection.insert_one(discussion.dict())
        discussion_dict = discussion.dict()
        discussion_dict["_id"] = result.inserted_id
        
        return discussion_dict
    
    async def get_discussions(self, discussion_type: Optional[DiscussionType] = None,
                            topic_id: Optional[str] = None, 
                            limit: int = 20, offset: int = 0,
                            sort_by: str = "created_at") -> List[Dict[str, Any]]:
        """Get discussions with filtering and pagination"""
        
        filter_query = {}
        if discussion_type:
            filter_query["discussion_type"] = discussion_type.value
        if topic_id:
            filter_query["topic_id"] = topic_id
        
        sort_direction = -1 if sort_by in ["created_at", "upvotes", "reply_count"] else 1
        
        discussions = await self.discussions_collection.find(filter_query)\
            .sort(sort_by, sort_direction)\
            .skip(offset)\
            .limit(limit)\
            .to_list(None)
        
        return discussions
    
    async def add_discussion_reply(self, discussion_id: str, content: str, 
                                 author_id: str, parent_reply_id: Optional[str] = None) -> Dict[str, Any]:
        """Add a reply to a discussion"""
        
        # Get author info
        author = await self.user_profiles_collection.find_one({"id": author_id})
        if not author:
            raise ValueError("Author not found")
        
        # Verify discussion exists
        discussion = await self.discussions_collection.find_one({"id": discussion_id})
        if not discussion:
            raise ValueError("Discussion not found")
        
        reply = DiscussionReply(
            discussion_id=discussion_id,
            content=content,
            author_id=author_id,
            author_username=author["username"],
            parent_reply_id=parent_reply_id
        )
        
        result = await self.discussion_replies_collection.insert_one(reply.dict())
        
        # Update discussion reply count
        await self.discussions_collection.update_one(
            {"id": discussion_id},
            {"$inc": {"reply_count": 1}}
        )
        
        reply_dict = reply.dict()
        reply_dict["_id"] = result.inserted_id
        
        return reply_dict
    
    async def vote_discussion(self, discussion_id: str, user_id: str, vote_type: str) -> Dict[str, Any]:
        """Vote on a discussion (upvote/downvote)"""
        
        if vote_type not in ["upvote", "downvote"]:
            raise ValueError("Invalid vote type")
        
        # For now, simple implementation - in production, track user votes to prevent double voting
        update_field = "upvotes" if vote_type == "upvote" else "downvotes"
        
        result = await self.discussions_collection.update_one(
            {"id": discussion_id},
            {"$inc": {update_field: 1}}
        )
        
        if result.matched_count == 0:
            raise ValueError("Discussion not found")
        
        # Get updated discussion
        discussion = await self.discussions_collection.find_one({"id": discussion_id})
        return discussion
    
    async def vote_reply(self, reply_id: str, user_id: str, vote_type: str) -> Dict[str, Any]:
        """Vote on a discussion reply"""
        
        if vote_type not in ["upvote", "downvote"]:
            raise ValueError("Invalid vote type")
        
        update_field = "upvotes" if vote_type == "upvote" else "downvotes"
        
        result = await self.discussion_replies_collection.update_one(
            {"id": reply_id},
            {"$inc": {update_field: 1}}
        )
        
        if result.matched_count == 0:
            raise ValueError("Reply not found")
        
        # Get updated reply
        reply = await self.discussion_replies_collection.find_one({"id": reply_id})
        return reply
    
    async def create_challenge(self, title: str, description: str, creator_id: str,
                             challenge_type: ChallengeType, topic_id: Optional[str] = None,
                             duration_days: int = 7, max_participants: int = 100,
                             rules: Dict[str, Any] = None, prizes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new peer challenge"""
        
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=duration_days)
        
        challenge = Challenge(
            title=title,
            description=description,
            challenge_type=challenge_type,
            creator_id=creator_id,
            topic_id=topic_id,
            max_participants=max_participants,
            start_date=start_date,
            end_date=end_date,
            rules=rules or {},
            prizes=prizes or {}
        )
        
        result = await self.challenges_collection.insert_one(challenge.dict())
        challenge_dict = challenge.dict()
        challenge_dict["_id"] = result.inserted_id
        
        return challenge_dict
    
    async def join_challenge(self, challenge_id: str, user_id: str) -> Dict[str, Any]:
        """Join a challenge"""
        
        # Check if challenge exists and is active
        challenge = await self.challenges_collection.find_one({"id": challenge_id, "is_active": True})
        if not challenge:
            raise ValueError("Challenge not found or not active")
        
        # Check if challenge is full
        if len(challenge.get("participants", [])) >= challenge["max_participants"]:
            raise ValueError("Challenge is full")
        
        # Check if user already joined
        existing_participant = await self.challenge_participants_collection.find_one({
            "challenge_id": challenge_id,
            "user_id": user_id
        })
        if existing_participant:
            raise ValueError("User already joined this challenge")
        
        # Get user info
        user = await self.user_profiles_collection.find_one({"id": user_id})
        if not user:
            raise ValueError("User not found")
        
        # Create participant record
        participant = ChallengeParticipant(
            challenge_id=challenge_id,
            user_id=user_id,
            username=user["username"]
        )
        
        await self.challenge_participants_collection.insert_one(participant.dict())
        
        # Update challenge participants list
        await self.challenges_collection.update_one(
            {"id": challenge_id},
            {"$push": {"participants": user_id}}
        )
        
        return participant.dict()
    
    async def get_active_challenges(self, user_id: Optional[str] = None, 
                                  challenge_type: Optional[ChallengeType] = None,
                                  limit: int = 20) -> List[Dict[str, Any]]:
        """Get active challenges"""
        
        filter_query = {
            "is_active": True,
            "end_date": {"$gt": datetime.utcnow()}
        }
        
        if challenge_type:
            filter_query["challenge_type"] = challenge_type.value
        
        challenges = await self.challenges_collection.find(filter_query)\
            .sort("created_at", -1)\
            .limit(limit)\
            .to_list(None)
        
        # Add participant info if user_id provided
        if user_id:
            for challenge in challenges:
                participant = await self.challenge_participants_collection.find_one({
                    "challenge_id": challenge["id"],
                    "user_id": user_id
                })
                challenge["user_participating"] = participant is not None
        
        return challenges
    
    async def update_challenge_progress(self, challenge_id: str, user_id: str, 
                                      progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user's progress in a challenge"""
        
        result = await self.challenge_participants_collection.update_one(
            {"challenge_id": challenge_id, "user_id": user_id},
            {"$set": {"progress": progress_data}}
        )
        
        if result.matched_count == 0:
            raise ValueError("Participant not found in challenge")
        
        # Get updated participant
        participant = await self.challenge_participants_collection.find_one({
            "challenge_id": challenge_id,
            "user_id": user_id
        })
        
        return participant
    
    async def create_study_group(self, name: str, description: str, creator_id: str,
                               topic_focus: List[str] = None, max_members: int = 20,
                               is_public: bool = True) -> Dict[str, Any]:
        """Create a new study group"""
        
        study_group = StudyGroup(
            name=name,
            description=description,
            creator_id=creator_id,
            members=[creator_id],  # Creator is automatically a member
            max_members=max_members,
            topic_focus=topic_focus or [],
            is_public=is_public
        )
        
        result = await self.study_groups_collection.insert_one(study_group.dict())
        study_group_dict = study_group.dict()
        study_group_dict["_id"] = result.inserted_id
        
        return study_group_dict
    
    async def join_study_group(self, group_id: str, user_id: str, 
                             invitation_code: Optional[str] = None) -> Dict[str, Any]:
        """Join a study group"""
        
        # Get study group
        group = await self.study_groups_collection.find_one({"id": group_id})
        if not group:
            raise ValueError("Study group not found")
        
        # Check if private group and invitation code required
        if not group["is_public"] and group["invitation_code"] != invitation_code:
            raise ValueError("Invalid invitation code")
        
        # Check if group is full
        if len(group.get("members", [])) >= group["max_members"]:
            raise ValueError("Study group is full")
        
        # Check if user already a member
        if user_id in group.get("members", []):
            raise ValueError("User already a member")
        
        # Add user to group
        await self.study_groups_collection.update_one(
            {"id": group_id},
            {"$push": {"members": user_id}}
        )
        
        # Add activity to group feed
        await self.add_study_group_activity(group_id, {
            "type": "member_joined",
            "user_id": user_id,
            "timestamp": datetime.utcnow()
        })
        
        return {"status": "success", "message": "Joined study group successfully"}
    
    async def add_study_group_activity(self, group_id: str, activity_data: Dict[str, Any]):
        """Add activity to study group feed"""
        
        await self.study_groups_collection.update_one(
            {"id": group_id},
            {"$push": {"activity_feed": activity_data}}
        )
    
    async def get_user_study_groups(self, user_id: str) -> List[Dict[str, Any]]:
        """Get study groups user is a member of"""
        
        groups = await self.study_groups_collection.find(
            {"members": user_id}
        ).to_list(None)
        
        return groups
    
    async def search_study_groups(self, query: str = "", topic_filter: List[str] = None,
                                public_only: bool = True, limit: int = 20) -> List[Dict[str, Any]]:
        """Search for study groups"""
        
        filter_query = {}
        
        if public_only:
            filter_query["is_public"] = True
        
        if query:
            filter_query["$or"] = [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        
        if topic_filter:
            filter_query["topic_focus"] = {"$in": topic_filter}
        
        groups = await self.study_groups_collection.find(filter_query)\
            .limit(limit)\
            .to_list(None)
        
        return groups