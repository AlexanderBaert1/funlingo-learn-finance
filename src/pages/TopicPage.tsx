
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import Navbar from "@/components/navbar";
import { LessonCard } from "@/components/lesson-card";
import { topics, lessons } from "@/data/topics";

const TopicPage = () => {
  const { topicId } = useParams();
  const [currentTopic, setCurrentTopic] = useState<any>(null);
  const [topicLessons, setTopicLessons] = useState<any[]>([]);
  
  useEffect(() => {
    const topic = topics.find(t => t.id === topicId);
    setCurrentTopic(topic);
    
    if (topicId && lessons[topicId as keyof typeof lessons]) {
      setTopicLessons(lessons[topicId as keyof typeof lessons]);
    } else {
      setTopicLessons([]);
    }
  }, [topicId]);
  
  if (!currentTopic) {
    return <div className="flex justify-center items-center min-h-screen">Loading topic...</div>;
  }
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar streak={3} gems={120} progress={15} />
      
      <main className="container mx-auto px-4 py-6">
        {/* Topic Header */}
        <section className="mb-8">
          <div className="flex items-center mb-4">
            <Link to="/" className="text-gray-500 hover:text-gray-700 mr-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="m15 18-6-6 6-6"></path>
              </svg>
            </Link>
            <h1 className="text-2xl font-bold">{currentTopic.title}</h1>
          </div>
          
          <div 
            className="rounded-xl p-6 text-white mb-4"
            style={{ backgroundColor: currentTopic.color }}
          >
            <div className="flex flex-col md:flex-row items-center">
              <div className="md:w-1/4 flex justify-center mb-4 md:mb-0">
                <div 
                  className="w-24 h-24 rounded-full bg-white/20 flex items-center justify-center"
                >
                  <div 
                    className="text-4xl"
                    dangerouslySetInnerHTML={{ __html: currentTopic.icon }}
                  />
                </div>
              </div>
              
              <div className="md:w-3/4">
                <h2 className="text-xl font-bold mb-2">{currentTopic.title}</h2>
                <p className="text-white/90 mb-4">{currentTopic.description}</p>
                
                {currentTopic.progress > 0 && (
                  <div className="mb-3">
                    <div className="flex justify-between text-sm mb-1">
                      <span>Progress</span>
                      <span>{currentTopic.progress}%</span>
                    </div>
                    <div className="w-full bg-white/30 rounded-full h-2">
                      <div 
                        className="h-2 rounded-full bg-white" 
                        style={{ width: `${currentTopic.progress}%` }}
                      ></div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>
        
        {/* Lessons */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">Lessons</h2>
            {currentTopic.progress > 0 && (
              <Button variant="outline" className="text-sm">Reset Progress</Button>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {topicLessons.length > 0 ? (
              topicLessons.map((lesson) => (
                <LessonCard 
                  key={lesson.id} 
                  lesson={lesson} 
                  topicColor={currentTopic.color} 
                />
              ))
            ) : (
              <div className="col-span-2 text-center py-12">
                <p className="text-gray-500">No lessons available for this topic yet.</p>
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
};

export default TopicPage;
