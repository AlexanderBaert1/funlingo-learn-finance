
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { TopicCard } from "@/components/topic-card";
import { topics } from "@/data/topics";

const Lessons = () => {
  const [streak, setStreak] = useState(3);
  const [gems, setGems] = useState(120);
  const [progress, setProgress] = useState(15);
  
  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="bg-white shadow-sm p-4 sticky top-0 z-10">
        <h1 className="text-xl font-bold text-center">Lessons</h1>
      </div>
      
      <main className="container mx-auto px-4 py-4">
        {/* Hero Section */}
        <section className="mb-6">
          <Card className="overflow-hidden bg-gradient-to-r from-finlingo-primary to-finlingo-secondary">
            <CardContent className="p-4">
              <div className="flex flex-col items-center">
                <div className="text-white mb-4 text-center">
                  <h2 className="text-xl font-bold mb-2">Welcome to Finlingo!</h2>
                  <p className="text-sm opacity-90 mb-4">
                    Learn personal finance through fun, bite-sized lessons.
                  </p>
                  <div className="flex flex-col gap-2">
                    <Link to="/topic/finance-basics">
                      <Button size="sm" className="bg-white text-finlingo-primary hover:bg-gray-100 w-full">
                        Start Today's Lesson
                      </Button>
                    </Link>
                    <Link to="#topics">
                      <Button size="sm" className="bg-white/20 text-white border border-white hover:bg-white hover:text-finlingo-primary transition-all w-full">
                        View All Topics
                      </Button>
                    </Link>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>
        
        {/* Daily Progress */}
        <section className="mb-6">
          <h3 className="text-lg font-bold mb-3">Your Progress</h3>
          <Card>
            <CardContent className="p-4">
              <div className="grid grid-cols-1 gap-4">
                <div className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-finlingo-primary/10 flex items-center justify-center mr-3">
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
                  <div className="flex-1">
                    <p className="font-semibold text-sm">{streak} Day Streak</p>
                    <p className="text-xs text-gray-500">Keep it going!</p>
                  </div>
                </div>
                
                <div className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-finlingo-secondary/10 flex items-center justify-center mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4CA35A" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M6 3h12l4 6-10 13L2 9Z"></path>
                      <path d="M12 22V9"></path>
                      <path d="m12 9 4-6"></path>
                      <path d="m12 9-4-6"></path>
                    </svg>
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold text-sm">{gems} Gems</p>
                    <p className="text-xs text-gray-500">Earn more by completing lessons</p>
                  </div>
                </div>
                
                <div className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-finlingo-secondary/10 flex items-center justify-center mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4CA35A" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="m22 10-10.1 5.7a3 3 0 0 1-3 0L2 12"></path>
                      <path d="M6 12v6a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-6"></path>
                      <path d="M2 8.5 12 14l10-5.5"></path>
                      <path d="M12 14v8"></path>
                      <path d="M19 5 12 9 5 5l7-4Z"></path>
                    </svg>
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold text-sm">1 of 6 Topics</p>
                    <p className="text-xs text-gray-500">Continue learning</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>
        
        {/* Topic Cards */}
        <section id="topics">
          <h3 className="text-lg font-bold mb-3">Finance Topics</h3>
          
          <div className="grid grid-cols-1 gap-4">
            {topics.map((topic) => (
              <TopicCard key={topic.id} topic={topic} />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
};

export default Lessons;
