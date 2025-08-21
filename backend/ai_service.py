import os
import json
from typing import Dict, List, Any, Optional
from emergentintegrations.llm.chat import LlmChat, UserMessage
from models import QuestionType, AIGeneratedQuestion, AIRecommendation
import uuid
from datetime import datetime

class AIService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    def _create_chat_session(self, system_message: str) -> LlmChat:
        """Create a new LLM chat session with Claude Sonnet 4"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=str(uuid.uuid4()),
            system_message=system_message
        )
        # Use Claude Sonnet 4 as specified by user
        chat.with_model("anthropic", "claude-sonnet-4-20250514")
        return chat
    
    async def generate_questions(self, topic_id: str, lesson_id: str, 
                               difficulty: int, question_type: QuestionType,
                               count: int = 5, context: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate AI-powered questions for a specific topic and lesson"""
        
        system_message = """You are an expert financial education content creator. Your task is to generate high-quality, educational questions that help users learn personal finance concepts effectively.

Guidelines:
1. Questions should be practical and relevant to real-world financial situations
2. Provide clear, accurate explanations that teach concepts
3. Use appropriate difficulty levels (1=beginner, 5=advanced)
4. Include helpful hints when appropriate
5. Make questions engaging and scenario-based when possible
6. Ensure all financial information is accurate and up-to-date

Return responses in valid JSON format only."""

        # Topic context mapping
        topic_contexts = {
            "basics": "Personal Finance Fundamentals - budgeting, income, expenses, assets, liabilities, net worth",
            "budgeting": "Budgeting and Money Management - creating budgets, tracking expenses, budget categories",
            "saving": "Saving Strategies - emergency funds, savings goals, high-yield accounts, compound interest",
            "investing": "Investment Basics - stocks, bonds, mutual funds, ETFs, risk management, portfolio diversification",
            "credit": "Credit and Debt Management - credit scores, credit cards, loans, debt payoff strategies",
            "taxes": "Tax Planning and Preparation - tax basics, deductions, tax-advantaged accounts"
        }
        
        topic_context = topic_contexts.get(topic_id, "General personal finance")
        
        question_type_instructions = {
            QuestionType.MULTIPLE_CHOICE: "Create multiple choice questions with 4 options, one correct answer",
            QuestionType.FILL_BLANK: "Create fill-in-the-blank questions with single word or short phrase answers",
            QuestionType.TRUE_FALSE: "Create true/false questions with detailed explanations",
            QuestionType.SCENARIO: "Create scenario-based questions with real-world financial situations",
            QuestionType.CALCULATION: "Create calculation questions involving financial math"
        }
        
        user_prompt = f"""
Generate {count} {question_type.value} questions for the topic "{topic_context}".

Requirements:
- Difficulty level: {difficulty}/5
- Question type: {question_type_instructions.get(question_type, 'Standard questions')}
- Context: {context if context else 'General lesson content'}

For each question, provide:
1. question: The main question text
2. type: "{question_type.value}"
3. options: Array of 4 options (for multiple choice only)
4. correct_answer: The correct answer
5. explanation: Detailed explanation (2-3 sentences)
6. hints: Array of 1-2 helpful hints
7. difficulty: {difficulty}
8. tags: Array of relevant keywords

Return as JSON array of question objects.
"""
        
        try:
            chat = self._create_chat_session(system_message)
            user_message = UserMessage(text=user_prompt)
            response = await chat.send_message(user_message)
            
            # Parse the JSON response
            questions = json.loads(response)
            
            # Validate and enhance questions
            enhanced_questions = []
            for q in questions:
                enhanced_q = {
                    "id": str(uuid.uuid4()),
                    "lesson_id": lesson_id,
                    "topic_id": topic_id,
                    "question": q.get("question", ""),
                    "type": question_type.value,
                    "options": q.get("options", []) if question_type == QuestionType.MULTIPLE_CHOICE else None,
                    "correct_answer": q.get("correct_answer", ""),
                    "explanation": q.get("explanation", ""),
                    "difficulty": difficulty,
                    "xp_reward": difficulty * 5,  # More XP for harder questions
                    "hints": q.get("hints", []),
                    "tags": q.get("tags", []),
                    "is_ai_generated": True,
                    "scenario_context": context
                }
                enhanced_questions.append(enhanced_q)
            
            return enhanced_questions
            
        except Exception as e:
            print(f"Error generating questions: {e}")
            return []
    
    async def generate_personalized_recommendations(self, user_id: str, 
                                                 user_progress: Dict[str, Any],
                                                 learning_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate personalized learning recommendations based on user progress"""
        
        system_message = """You are an AI learning coach specializing in personalized financial education. Analyze user progress and learning patterns to provide tailored recommendations that optimize their learning journey.

Consider:
1. User's current skill level and progress
2. Learning patterns and preferences
3. Areas that need improvement
4. Optimal learning pace and difficulty progression
5. Motivation and engagement factors

Provide actionable, personalized recommendations."""

        user_prompt = f"""
Analyze this user's learning data and provide personalized recommendations:

User Progress: {json.dumps(user_progress)}
Learning History: {json.dumps(learning_history[-10:])}  # Last 10 activities

Provide 5-8 recommendations in the following categories:
1. Next lessons to focus on
2. Topics to review
3. Practice exercises
4. Challenge opportunities
5. Community engagement

For each recommendation, provide:
- type: "lesson", "topic", "practice", "review", "challenge", or "community"
- content_id: relevant ID
- title: recommendation title
- reason: why this is recommended (1-2 sentences)
- priority: 1-5 (5 = highest priority)
- confidence_score: 0.0-1.0

Return as JSON array.
"""
        
        try:
            chat = self._create_chat_session(system_message)
            user_message = UserMessage(text=user_prompt)
            response = await chat.send_message(user_message)
            
            recommendations = json.loads(response)
            
            # Enhance recommendations with IDs
            enhanced_recommendations = []
            for rec in recommendations:
                enhanced_rec = {
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "type": rec.get("type", "lesson"),
                    "content_id": rec.get("content_id", ""),
                    "title": rec.get("title", ""),
                    "reason": rec.get("reason", ""),
                    "priority": rec.get("priority", 3),
                    "confidence_score": rec.get("confidence_score", 0.5),
                    "is_viewed": False,
                    "is_accepted": False
                }
                enhanced_recommendations.append(enhanced_rec)
            
            return enhanced_recommendations
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return []
    
    async def generate_learning_path(self, user_id: str, 
                                   goals: List[str], 
                                   current_level: int,
                                   available_time: int) -> Dict[str, Any]:
        """Generate a personalized learning path"""
        
        system_message = """You are an expert curriculum designer for financial education. Create personalized learning paths that efficiently guide users toward their financial literacy goals while respecting their time constraints and current knowledge level."""

        user_prompt = f"""
Create a personalized learning path for:

Goals: {goals}
Current Level: {current_level}/5
Available Time: {available_time} minutes per day

Design a learning path that includes:
1. Recommended sequence of topics and lessons
2. Estimated timeline for completion
3. Difficulty progression strategy
4. Checkpoint assessments
5. Practice opportunities

Provide the path structure with:
- name: descriptive path name
- description: overview of the path
- estimated_completion: days to complete
- recommended_lessons: array of lesson objects with order, priority, and rationale
- milestones: key checkpoints with goals
- difficulty_adjustment: factor for personalizing question difficulty

Return as JSON object.
"""
        
        try:
            chat = self._create_chat_session(system_message)
            user_message = UserMessage(text=user_prompt)
            response = await chat.send_message(user_message)
            
            learning_path = json.loads(response)
            
            # Add metadata
            learning_path["id"] = str(uuid.uuid4())
            learning_path["user_id"] = user_id
            learning_path["is_active"] = True
            learning_path["progress"] = 0.0
            
            return learning_path
            
        except Exception as e:
            print(f"Error generating learning path: {e}")
            return {}
    
    async def analyze_user_performance(self, user_id: str, 
                                     performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user performance and provide insights"""
        
        system_message = """You are a learning analytics expert. Analyze user performance data to identify strengths, weaknesses, learning patterns, and provide actionable insights for improvement."""

        user_prompt = f"""
Analyze this user's performance data:

{json.dumps(performance_data)}

Provide analysis including:
1. Strengths and areas of mastery
2. Areas needing improvement
3. Learning patterns and preferences
4. Difficulty adjustment recommendations
5. Study strategy suggestions
6. Motivation insights

Return detailed analysis as JSON object with specific recommendations.
"""
        
        try:
            chat = self._create_chat_session(system_message)
            user_message = UserMessage(text=user_prompt)
            response = await chat.send_message(user_message)
            
            analysis = json.loads(response)
            return analysis
            
        except Exception as e:
            print(f"Error analyzing performance: {e}")
            return {}

    async def generate_adaptive_content(self, user_id: str,
                                      weak_topics: List[str],
                                      preferred_difficulty: int) -> List[Dict[str, Any]]:
        """Generate adaptive practice content based on weak areas"""
        
        system_message = """You are an adaptive learning specialist. Create targeted practice content that addresses specific learning gaps while maintaining appropriate challenge levels."""

        user_prompt = f"""
Generate targeted practice content for these weak areas: {weak_topics}
Preferred difficulty: {preferred_difficulty}/5

Create 3-5 practice exercises that:
1. Target the specific weak topics
2. Use varied question types for engagement
3. Include progressive difficulty
4. Provide extensive explanations
5. Connect concepts to real-world applications

Return as JSON array of practice questions.
"""
        
        try:
            chat = self._create_chat_session(system_message)
            user_message = UserMessage(text=user_prompt)
            response = await chat.send_message(user_message)
            
            content = json.loads(response)
            
            # Add metadata to each item
            for item in content:
                item["id"] = str(uuid.uuid4())
                item["user_id"] = user_id
                item["is_adaptive"] = True
                item["target_topics"] = weak_topics
            
            return content
            
        except Exception as e:
            print(f"Error generating adaptive content: {e}")
            return []