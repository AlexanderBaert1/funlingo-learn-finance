
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/navbar";

const Profile = () => {
  const [streak, setStreak] = useState(3);
  const [gems, setGems] = useState(120);
  const [progress, setProgress] = useState(15);
  const [completedTopics, setCompletedTopics] = useState(1);
  const [totalTopics, setTotalTopics] = useState(6);
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar streak={streak} gems={gems} progress={progress} />
      
      <main className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">My Profile</h1>
          <Button variant="outline">Edit Profile</Button>
        </div>
        
        {/* User Profile Card */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <Card className="lg:col-span-1">
            <CardContent className="pt-6">
              <div className="flex flex-col items-center">
                <div className="w-24 h-24 bg-finlingo-primary/10 rounded-full flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#3D99EC" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
                <h2 className="text-xl font-bold mb-1">John Doe</h2>
                <p className="text-gray-500 mb-4">john.doe@example.com</p>
                <div className="flex gap-2 mb-4">
                  <Badge className="bg-finlingo-primary">Beginner</Badge>
                  <Badge className="bg-finlingo-secondary">{completedTopics}/{totalTopics} Topics</Badge>
                </div>
                <Link to="/settings">
                  <Button variant="outline" size="sm">Account Settings</Button>
                </Link>
              </div>
            </CardContent>
          </Card>
          
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>Learning Statistics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="bg-white p-4 rounded-lg border">
                  <div className="flex items-center mb-2">
                    <div className="w-10 h-10 rounded-full bg-finlingo-primary/10 flex items-center justify-center mr-3">
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3D99EC" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M14.5 4.5 12 2 9.5 4.5"></path>
                        <path d="m18 6-2-2"></path>
                        <path d="m8 6-2 2"></path>
                        <path d="M13.4 10H15a2 2 0 1 1 0 4h-4a1 1 0 0 0-1 1 1 1 0 0 0 1 1h4a4 4 0 1 0 0-8h-1.6"></path>
                        <path d="M9 15v1"></path>
                        <path d="M9 8v1"></path>
                        <path d="M9 12h12"></path>
                      </svg>
                    </div>
                    <div>
                      <p className="text-gray-500 text-sm">Current Streak</p>
                      <p className="font-bold text-xl">{streak} days</p>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500">Best streak: 5 days</p>
                </div>
                
                <div className="bg-white p-4 rounded-lg border">
                  <div className="flex items-center mb-2">
                    <div className="w-10 h-10 rounded-full bg-finlingo-secondary/10 flex items-center justify-center mr-3">
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4CA35A" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M6 3h12l4 6-10 13L2 9Z"></path>
                        <path d="M12 22V9"></path>
                        <path d="m12 9 4-6"></path>
                        <path d="m12 9-4-6"></path>
                      </svg>
                    </div>
                    <div>
                      <p className="text-gray-500 text-sm">Total Gems</p>
                      <p className="font-bold text-xl">{gems}</p>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500">Weekly goal: 300 gems</p>
                </div>
                
                <div className="bg-white p-4 rounded-lg border">
                  <div className="flex items-center mb-2">
                    <div className="w-10 h-10 rounded-full bg-finlingo-secondary/10 flex items-center justify-center mr-3">
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4CA35A" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="m22 10-10.1 5.7a3 3 0 0 1-3 0L2 12"></path>
                        <path d="M6 12v6a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-6"></path>
                        <path d="M2 8.5 12 14l10-5.5"></path>
                        <path d="M12 14v8"></path>
                        <path d="M19 5 12 9 5 5l7-4Z"></path>
                      </svg>
                    </div>
                    <div>
                      <p className="text-gray-500 text-sm">Lessons Completed</p>
                      <p className="font-bold text-xl">8</p>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500">Total available: 24 lessons</p>
                </div>
              </div>
              
              <div className="mb-6">
                <p className="text-gray-700 font-semibold mb-2">Weekly Activity</p>
                <div className="grid grid-cols-7 gap-1">
                  {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((day, i) => (
                    <div key={i} className="text-center">
                      <div className={`w-8 h-8 mx-auto mb-1 rounded-md flex items-center justify-center ${i < 3 ? 'bg-finlingo-primary text-white' : 'bg-gray-100'}`}>
                        {i < 3 && (
                          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                          </svg>
                        )}
                      </div>
                      <span className="text-xs text-gray-500">{day}</span>
                    </div>
                  ))}
                </div>
              </div>
              
              <div>
                <p className="text-gray-700 font-semibold mb-2">Topic Progress</p>
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Budgeting Basics</span>
                      <span>75%</span>
                    </div>
                    <Progress value={75} className="h-2" />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Investing 101</span>
                      <span>20%</span>
                    </div>
                    <Progress value={20} className="h-2" />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Debt Management</span>
                      <span>0%</span>
                    </div>
                    <Progress value={0} className="h-2" />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
        
        {/* Achievements */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Achievements</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
              {[
                { name: "First Lesson", unlocked: true, icon: "🏆" },
                { name: "3-Day Streak", unlocked: true, icon: "🔥" },
                { name: "Budget Master", unlocked: false, icon: "💰" },
                { name: "Investing Pro", unlocked: false, icon: "📈" },
                { name: "Debt Destroyer", unlocked: false, icon: "✂️" }
              ].map((achievement, i) => (
                <div 
                  key={i} 
                  className={`flex flex-col items-center p-4 rounded-lg ${
                    achievement.unlocked 
                      ? 'bg-white border border-finlingo-primary/20' 
                      : 'bg-gray-100 opacity-60'
                  }`}
                >
                  <div className={`
                    w-12 h-12 rounded-full flex items-center justify-center mb-2 text-2xl
                    ${achievement.unlocked ? 'bg-finlingo-primary/10' : 'bg-gray-200'}
                  `}>
                    {achievement.icon}
                  </div>
                  <p className="text-sm font-medium text-center">{achievement.name}</p>
                  <p className="text-xs text-gray-500">
                    {achievement.unlocked ? 'Unlocked' : 'Locked'}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default Profile;
