#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Enhanced Finlingo API
Tests all new features including AI, gamification, and community features
"""

import asyncio
import aiohttp
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List

# Backend URL from environment
BACKEND_URL = "https://finlingo-hub.preview.emergentagent.com/api"

class FinlingoBackendTester:
    def __init__(self):
        self.session = None
        self.test_user_id = None
        self.test_discussion_id = None
        self.test_results = []
        
    async def setup_session(self):
        """Setup HTTP session"""
        self.session = aiohttp.ClientSession()
        
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
    async def test_health_check(self):
        """Test health check endpoint"""
        try:
            async with self.session.get(f"{BACKEND_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    if "status" in data and data["status"] == "healthy":
                        self.log_test("Health Check", True, "Backend is healthy", data)
                        return True
                    else:
                        self.log_test("Health Check", False, f"Unexpected response format: {data}")
                        return False
                else:
                    self.log_test("Health Check", False, f"HTTP {response.status}")
                    return False
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False
    
    async def test_user_creation(self):
        """Test user profile creation"""
        try:
            # Generate unique test user data
            test_username = f"testuser_{uuid.uuid4().hex[:8]}"
            test_email = f"test_{uuid.uuid4().hex[:8]}@finlingo.com"
            
            user_data = {
                "username": test_username,
                "email": test_email,
                "display_name": "Test User"
            }
            
            async with self.session.post(f"{BACKEND_URL}/users", json=user_data) as response:
                if response.status == 200:
                    data = await response.json()
                    if "id" in data and "username" in data:
                        self.test_user_id = data["id"]
                        self.log_test("User Creation", True, f"Created user with ID: {self.test_user_id}", data)
                        return True
                    else:
                        self.log_test("User Creation", False, f"Missing required fields in response: {data}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_test("User Creation", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_test("User Creation", False, f"Exception: {str(e)}")
            return False
    
    async def test_user_profile_retrieval(self):
        """Test user profile retrieval"""
        if not self.test_user_id:
            self.log_test("User Profile Retrieval", False, "No test user ID available")
            return False
            
        try:
            async with self.session.get(f"{BACKEND_URL}/users/{self.test_user_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    if "id" in data and data["id"] == self.test_user_id:
                        self.log_test("User Profile Retrieval", True, "Successfully retrieved user profile", data)
                        return True
                    else:
                        self.log_test("User Profile Retrieval", False, f"User ID mismatch: {data}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_test("User Profile Retrieval", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_test("User Profile Retrieval", False, f"Exception: {str(e)}")
            return False
    
    async def test_ai_question_generation(self):
        """Test AI question generation endpoint"""
        try:
            question_request = {
                "topic_id": "basics",
                "lesson_id": "basics_intro",
                "difficulty": 2,
                "question_type": "multiple-choice",
                "context": "Introduction to personal finance fundamentals"
            }
            
            async with self.session.post(f"{BACKEND_URL}/ai/generate-questions", json=question_request) as response:
                if response.status == 200:
                    data = await response.json()
                    if "questions" in data and isinstance(data["questions"], list) and len(data["questions"]) > 0:
                        # Validate question structure
                        first_question = data["questions"][0]
                        required_fields = ["id", "question", "type", "correct_answer", "explanation"]
                        if all(field in first_question for field in required_fields):
                            self.log_test("AI Question Generation", True, f"Generated {len(data['questions'])} questions", data)
                            return True
                        else:
                            missing_fields = [field for field in required_fields if field not in first_question]
                            self.log_test("AI Question Generation", False, f"Missing fields in question: {missing_fields}")
                            return False
                    else:
                        self.log_test("AI Question Generation", False, f"Invalid response format: {data}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_test("AI Question Generation", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_test("AI Question Generation", False, f"Exception: {str(e)}")
            return False
    
    async def test_achievements_endpoint(self):
        """Test achievements retrieval"""
        try:
            async with self.session.get(f"{BACKEND_URL}/achievements") as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list):
                        if len(data) > 0:
                            # Validate achievement structure
                            first_achievement = data[0]
                            required_fields = ["id", "name", "description", "type", "requirement"]
                            if all(field in first_achievement for field in required_fields):
                                self.log_test("Achievements Endpoint", True, f"Retrieved {len(data)} achievements", {"count": len(data)})
                                return True
                            else:
                                missing_fields = [field for field in required_fields if field not in first_achievement]
                                self.log_test("Achievements Endpoint", False, f"Missing fields in achievement: {missing_fields}")
                                return False
                        else:
                            self.log_test("Achievements Endpoint", True, "No achievements found (empty list)", data)
                            return True
                    else:
                        self.log_test("Achievements Endpoint", False, f"Expected list, got: {type(data)}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_test("Achievements Endpoint", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_test("Achievements Endpoint", False, f"Exception: {str(e)}")
            return False
    
    async def test_global_leaderboard(self):
        """Test global leaderboard endpoint"""
        try:
            async with self.session.get(f"{BACKEND_URL}/leaderboard/global") as response:
                if response.status == 200:
                    data = await response.json()
                    if "leaderboard" in data and "type" in data:
                        if data["type"] == "global" and isinstance(data["leaderboard"], list):
                            self.log_test("Global Leaderboard", True, f"Retrieved leaderboard with {len(data['leaderboard'])} entries", {"count": len(data["leaderboard"])})
                            return True
                        else:
                            self.log_test("Global Leaderboard", False, f"Invalid leaderboard format: {data}")
                            return False
                    else:
                        self.log_test("Global Leaderboard", False, f"Missing required fields: {data}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_test("Global Leaderboard", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_test("Global Leaderboard", False, f"Exception: {str(e)}")
            return False
    
    async def test_discussion_creation(self):
        """Test discussion creation"""
        if not self.test_user_id:
            self.log_test("Discussion Creation", False, "No test user ID available")
            return False
            
        try:
            discussion_data = {
                "title": f"Test Discussion {uuid.uuid4().hex[:8]}",
                "content": "This is a test discussion about personal finance basics. What are your thoughts on budgeting strategies?",
                "author_id": self.test_user_id,
                "discussion_type": "general",
                "topic_id": "basics",
                "tags": ["budgeting", "basics", "discussion"]
            }
            
            async with self.session.post(f"{BACKEND_URL}/discussions", params=discussion_data) as response:
                if response.status == 200:
                    data = await response.json()
                    if "id" in data and "title" in data and "author_id" in data:
                        self.test_discussion_id = data["id"]
                        self.log_test("Discussion Creation", True, f"Created discussion with ID: {self.test_discussion_id}", data)
                        return True
                    else:
                        self.log_test("Discussion Creation", False, f"Missing required fields in response: {data}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_test("Discussion Creation", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_test("Discussion Creation", False, f"Exception: {str(e)}")
            return False
    
    async def test_discussions_retrieval(self):
        """Test discussions retrieval"""
        try:
            async with self.session.get(f"{BACKEND_URL}/discussions") as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list):
                        self.log_test("Discussions Retrieval", True, f"Retrieved {len(data)} discussions", {"count": len(data)})
                        return True
                    else:
                        self.log_test("Discussions Retrieval", False, f"Expected list, got: {type(data)}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_test("Discussions Retrieval", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_test("Discussions Retrieval", False, f"Exception: {str(e)}")
            return False
    
    async def test_lesson_completion_flow(self):
        """Test lesson completion flow"""
        if not self.test_user_id:
            self.log_test("Lesson Completion Flow", False, "No test user ID available")
            return False
            
        try:
            # Simulate lesson completion
            completion_data = {
                "lesson_id": "basics_lesson_1",
                "topic_id": "basics",
                "question_responses": [
                    {
                        "question_id": "q1",
                        "user_answer": "A",
                        "is_correct": True,
                        "time_taken": 30
                    },
                    {
                        "question_id": "q2", 
                        "user_answer": "B",
                        "is_correct": False,
                        "time_taken": 45
                    }
                ],
                "total_time": 300,
                "user_id": self.test_user_id
            }
            
            async with self.session.post(f"{BACKEND_URL}/lessons/basics_lesson_1/complete", json=completion_data) as response:
                if response.status == 200:
                    data = await response.json()
                    required_fields = ["score", "xp_earned", "gems_earned"]
                    if all(field in data for field in required_fields):
                        self.log_test("Lesson Completion Flow", True, f"Lesson completed successfully. Score: {data['score']}%, XP: {data['xp_earned']}", data)
                        return True
                    else:
                        missing_fields = [field for field in required_fields if field not in data]
                        self.log_test("Lesson Completion Flow", False, f"Missing fields in response: {missing_fields}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_test("Lesson Completion Flow", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_test("Lesson Completion Flow", False, f"Exception: {str(e)}")
            return False
    
    async def test_user_progress_analytics(self):
        """Test user progress analytics"""
        if not self.test_user_id:
            self.log_test("User Progress Analytics", False, "No test user ID available")
            return False
            
        try:
            async with self.session.get(f"{BACKEND_URL}/users/{self.test_user_id}/progress") as response:
                if response.status == 200:
                    data = await response.json()
                    required_sections = ["profile", "statistics"]
                    if all(section in data for section in required_sections):
                        self.log_test("User Progress Analytics", True, "Retrieved user progress analytics", data)
                        return True
                    else:
                        missing_sections = [section for section in required_sections if section not in data]
                        self.log_test("User Progress Analytics", False, f"Missing sections: {missing_sections}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_test("User Progress Analytics", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_test("User Progress Analytics", False, f"Exception: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Enhanced Finlingo Backend Tests")
        print(f"🔗 Testing Backend URL: {BACKEND_URL}")
        print("=" * 60)
        
        await self.setup_session()
        
        try:
            # Core functionality tests
            await self.test_health_check()
            
            # User management tests
            await self.test_user_creation()
            await self.test_user_profile_retrieval()
            
            # AI features tests
            await self.test_ai_question_generation()
            
            # Gamification tests
            await self.test_achievements_endpoint()
            await self.test_global_leaderboard()
            
            # Community features tests
            await self.test_discussion_creation()
            await self.test_discussions_retrieval()
            
            # Enhanced educational features tests
            await self.test_lesson_completion_flow()
            await self.test_user_progress_analytics()
            
        finally:
            await self.cleanup_session()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['details']}")
        
        print("\n" + "=" * 60)
        
        return passed_tests, failed_tests, self.test_results

async def main():
    """Main test execution"""
    tester = FinlingoBackendTester()
    passed, failed, results = await tester.run_all_tests()
    
    # Save detailed results to file
    with open("/app/backend_test_results.json", "w") as f:
        json.dump({
            "summary": {
                "total_tests": len(results),
                "passed": passed,
                "failed": failed,
                "success_rate": (passed/len(results))*100 if results else 0,
                "timestamp": datetime.now().isoformat()
            },
            "detailed_results": results
        }, f, indent=2)
    
    print(f"📄 Detailed results saved to: /app/backend_test_results.json")
    
    # Return appropriate exit code
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)