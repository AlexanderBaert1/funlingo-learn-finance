
import { Card, CardContent } from "@/components/ui/card";
import { Heart, MessageCircle, Share2 } from 'lucide-react';

const NewsFeed = () => {
  const newsItems = [
    {
      id: 1,
      title: "5 Tips for Building Your Emergency Fund",
      content: "Start small and be consistent. Even $5 a week can make a difference over time...",
      author: "Sarah Johnson",
      time: "2 hours ago",
      likes: 24,
      comments: 8
    },
    {
      id: 2,
      title: "Why Young Adults Should Start Investing Now",
      content: "The power of compound interest is real. Starting early, even with small amounts, can lead to...",
      author: "Mike Chen",
      time: "5 hours ago",
      likes: 42,
      comments: 15
    },
    {
      id: 3,
      title: "Understanding Credit Scores: What You Need to Know",
      content: "Your credit score affects many aspects of your financial life. Here's how to improve it...",
      author: "Emily Davis",
      time: "1 day ago",
      likes: 67,
      comments: 23
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="bg-white shadow-sm p-4 sticky top-0 z-10">
        <h1 className="text-xl font-bold text-center">News Feed</h1>
      </div>
      
      <div className="container mx-auto px-4 py-4 space-y-4">
        {newsItems.map((item) => (
          <Card key={item.id} className="overflow-hidden">
            <CardContent className="p-4">
              <div className="flex items-center mb-3">
                <div className="w-8 h-8 bg-finlingo-primary rounded-full flex items-center justify-center text-white text-sm font-bold">
                  {item.author.split(' ').map(name => name[0]).join('')}
                </div>
                <div className="ml-3">
                  <p className="font-semibold text-sm">{item.author}</p>
                  <p className="text-xs text-gray-500">{item.time}</p>
                </div>
              </div>
              
              <h3 className="font-bold text-lg mb-2">{item.title}</h3>
              <p className="text-gray-600 text-sm mb-4">{item.content}</p>
              
              <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                <button className="flex items-center space-x-1 text-gray-500 hover:text-red-500 transition-colors">
                  <Heart size={18} />
                  <span className="text-sm">{item.likes}</span>
                </button>
                <button className="flex items-center space-x-1 text-gray-500 hover:text-finlingo-primary transition-colors">
                  <MessageCircle size={18} />
                  <span className="text-sm">{item.comments}</span>
                </button>
                <button className="flex items-center space-x-1 text-gray-500 hover:text-finlingo-primary transition-colors">
                  <Share2 size={18} />
                  <span className="text-sm">Share</span>
                </button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default NewsFeed;
