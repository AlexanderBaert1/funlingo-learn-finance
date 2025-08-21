import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

export interface Lesson {
  id: string;
  topicId: string;
  title: string;
  description: string;
  duration: number;
  xp: number;
  completed: boolean;
  locked?: boolean;
}

interface LessonCardProps {
  lesson: Lesson;
  topicColor: string;
}

export function LessonCard({ lesson, topicColor }: LessonCardProps) {
  return (
    <div className={`
      bg-white rounded-xl shadow-md p-5 
      ${lesson.locked ? 'opacity-70' : ''}
    `}>
      {/* Status Indicator */}
      <div className="flex justify-between items-center mb-3">
        <div className="flex items-center">
          {lesson.completed ? (
            <div className={`w-6 h-6 rounded-full flex items-center justify-center`} style={{backgroundColor: topicColor}}>
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
          ) : lesson.locked ? (
            <div className="w-6 h-6 rounded-full flex items-center justify-center bg-gray-200">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect width="18" height="11" x="3" y="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
          ) : (
            <div className={`w-6 h-6 rounded-full border-2`} style={{borderColor: topicColor}}></div>
          )}
          <span className="ml-2 text-sm font-semibold">{lesson.xp} XP</span>
        </div>
        
        <div className="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="mr-1">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <span className="text-xs text-gray-500">{lesson.duration} min</span>
        </div>
      </div>
      
      <h3 className="font-bold mb-2">{lesson.title}</h3>
      <p className="text-sm text-gray-600 mb-4">{lesson.description}</p>
      
      <div className="flex justify-end">
        {lesson.locked ? (
          <Button
            disabled={true}
            className="text-white bg-gray-400"
          >
            Locked
          </Button>
        ) : (
          <Link to={`/lesson/${lesson.topicId}/${lesson.id}`}>
            <Button
              className={`text-white ${lesson.completed ? 'bg-gray-400 hover:bg-gray-500' : ''}`}
              style={{backgroundColor: lesson.completed ? '' : topicColor}}
            >
              {lesson.completed ? 'Practice Again' : 'Start Lesson'}
            </Button>
          </Link>
        )}
      </div>
    </div>
  );
}

export default LessonCard;
