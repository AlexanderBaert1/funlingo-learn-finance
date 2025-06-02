import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Navbar from "@/components/navbar";
import { TopicCard } from "@/components/topic-card";
import { topics } from "@/data/topics";

const Index = () => {
  const [streak, setStreak] = useState(3);
  const [gems, setGems] = useState(120);
  const [progress, setProgress] = useState(15);
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-400 via-blue-500 to-blue-600">
      <Navbar streak={streak} gems={gems} progress={progress} />
      
      <main className="container mx-auto px-4 py-6">
        {/* Hero Section */}
        <section className="mb-10">
          <Card className="overflow-hidden bg-white/10 backdrop-blur-sm border-white/20">
            <CardContent className="p-6 sm:p-8">
              <div className="flex flex-col items-center">
                <div className="text-white mb-6 text-center">
                  <h1 className="text-3xl sm:text-4xl font-bold mb-2 animate-slide-up">Welcome to Finlingo!</h1>
                  <p className="text-lg opacity-90 mb-6 animate-slide-up" style={{animationDelay: "0.1s"}}>
                    Learn personal finance through fun, bite-sized lessons.
                  </p>
                  <div className="flex flex-wrap gap-4 justify-center animate-slide-up" style={{animationDelay: "0.2s"}}>
                    <Link to="/topic/finance-basics">
                      <Button size="lg" className="bg-white text-green-600 hover:bg-gray-100 font-semibold">
                        Start Today's Lesson
                      </Button>
                    </Link>
                    <Link to="#topics">
                      <Button size="lg" className="bg-white/20 text-white border-2 border-white hover:bg-white hover:text-blue-600 transition-all font-semibold">
                        View All Topics
                      </Button>
                    </Link>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>
        
        {/* Daily Streak */}
        <section className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-white">Your Progress</h2>
            <Link to="/profile" className="text-white/90 text-sm font-semibold hover:text-white">View Details</Link>
          </div>
          <Card className="bg-white/95 backdrop-blur-sm">
            <CardContent className="p-6">
              <div className="flex flex-col sm:flex-row gap-6 sm:items-center">
                <div className="sm:w-1/3">
                  <div className="flex items-center mb-2">
                    <div className="w-8 h-8 rounded-full bg-finlingo-primary/10 flex items-center justify-center mr-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3D99EC" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M14.5 4.5 12 2 9.5 4.5"></path>
                        <path d="m18 6-2-2"></path>
                        <path d="m8 6-2 2"></path>
                        <path d="M13.4 10H15a2 2 0 1 1 0 4h-4a1 1 0 0 0-1 1 1 1 0 0 0 1 1h4a4 4 0 1 0 0-8h-1.6"></path>
                        <path d="M9 15v1"></path>
                        <path d="M9 8v1"></path>
                        <path d="M9 12h12"></path>
                      </svg>
                    </div>
                    <span className="font-semibold">{streak} Day Streak</span>
                  </div>
                  <p className="text-sm text-gray-500">Keep it going! Practice daily to build your streak.</p>
                </div>
                
                <div className="sm:w-1/3">
                  <div className="flex items-center mb-2">
                    <div className="w-8 h-8 rounded-full bg-finlingo-secondary/10 flex items-center justify-center mr-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4CA35A" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M6 3h12l4 6-10 13L2 9Z"></path>
                        <path d="M12 22V9"></path>
                        <path d="m12 9 4-6"></path>
                        <path d="m12 9-4-6"></path>
                      </svg>
                    </div>
                    <span className="font-semibold">{gems} Gems</span>
                  </div>
                  <p className="text-sm text-gray-500">Earn gems by completing lessons and challenges.</p>
                </div>
                
                <div className="sm:w-1/3">
                  <div className="flex items-center mb-2">
                    <div className="w-8 h-8 rounded-full bg-finlingo-secondary/10 flex items-center justify-center mr-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4CA35A" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="m22 10-10.1 5.7a3 3 0 0 1-3 0L2 12"></path>
                        <path d="M6 12v6a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-6"></path>
                        <path d="M2 8.5 12 14l10-5.5"></path>
                        <path d="M12 14v8"></path>
                        <path d="M19 5 12 9 5 5l7-4Z"></path>
                      </svg>
                    </div>
                    <span className="font-semibold">1 of 6 Topics Explored</span>
                  </div>
                  <p className="text-sm text-gray-500">Continue learning to unlock all finance topics.</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>
        
        {/* Topic Cards */}
        <section id="topics">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-white">Finance Topics</h2>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {topics.map((topic) => (
              <TopicCard key={topic.id} topic={topic} />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
};

export default Index;
