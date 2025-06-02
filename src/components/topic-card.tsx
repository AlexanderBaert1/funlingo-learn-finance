
import { Link } from 'react-router-dom';

export interface Topic {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  progress: number;
  locked?: boolean;
}

interface TopicCardProps {
  topic: Topic;
}

export function TopicCard({ topic }: TopicCardProps) {
  return (
    <Link 
      to={topic.locked ? "#" : `/topic/${topic.id}`}
      className={`
        relative flex flex-col items-center p-6 rounded-2xl 
        transition-transform transform hover:scale-105 
        ${topic.locked ? 'bg-white/40 cursor-not-allowed opacity-70' : 'bg-white/90 backdrop-blur-sm shadow-md hover:shadow-lg hover:bg-white/95'}
      `}
    >
      {topic.locked && (
        <div className="absolute top-3 right-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect width="18" height="11" x="3" y="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </div>
      )}
      
      <div 
        className={`w-16 h-16 rounded-full flex items-center justify-center mb-4`}
        style={{ backgroundColor: `${topic.color}15` }} // Light background using the color with opacity
      >
        <div 
          className="text-2xl"
          style={{ color: topic.color }}
          dangerouslySetInnerHTML={{ __html: topic.icon }}
        />
      </div>
      
      <h3 className="text-lg font-bold mb-1">{topic.title}</h3>
      <p className="text-sm text-gray-600 text-center mb-4">{topic.description}</p>
      
      {topic.progress > 0 && !topic.locked && (
        <div className="w-full bg-gray-200 rounded-full h-1.5 mb-1">
          <div 
            className="h-1.5 rounded-full" 
            style={{ width: `${topic.progress}%`, backgroundColor: topic.color }}
          ></div>
        </div>
      )}
      
      {topic.progress > 0 && !topic.locked && (
        <p className="text-xs text-gray-500">{topic.progress}% complete</p>
      )}
      
      {topic.locked && (
        <p className="text-xs text-gray-500 mt-2">Complete previous topics to unlock</p>
      )}
    </Link>
  );
}

export default TopicCard;
