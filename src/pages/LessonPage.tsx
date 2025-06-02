
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Heart, Star, Trophy } from 'lucide-react';
import { lessons } from "@/data/topics";
import { questionData } from "@/data/questions";
import { QuestionCard } from "@/components/question-card";
import { ResultModal } from "@/components/result-modal";

const LessonPage = () => {
  const { topicId, lessonId } = useParams();
  const navigate = useNavigate();
  
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [hearts, setHearts] = useState(3);
  const [showResult, setShowResult] = useState(false);
  const [lessonComplete, setLessonComplete] = useState(false);
  const [score, setScore] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [showFeedback, setShowFeedback] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  // Get current lesson and questions
  const topicLessons = lessons[topicId as keyof typeof lessons] || [];
  const currentLesson = topicLessons.find(lesson => lesson.id === lessonId);
  const questions = questionData[lessonId as keyof typeof questionData] || [];
  
  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  const handleAnswerSelect = (answer: string) => {
    setSelectedAnswer(answer);
  };

  const handleAnswerSubmit = () => {
    if (!selectedAnswer) return;

    const correct = selectedAnswer === currentQuestion.correctAnswer;
    setIsCorrect(correct);
    setShowFeedback(true);

    if (correct) {
      setScore(score + 10);
    } else {
      setHearts(hearts - 1);
    }

    setTimeout(() => {
      const newAnswers = [...answers, selectedAnswer];
      setAnswers(newAnswers);
      
      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
        setSelectedAnswer('');
        setShowFeedback(false);
      } else {
        setLessonComplete(true);
        setShowResult(true);
      }
    }, 2000);
  };

  const handleContinue = () => {
    if (hearts <= 0) {
      navigate(`/topic/${topicId}`);
      return;
    }
    
    if (lessonComplete) {
      navigate(`/topic/${topicId}`);
    }
  };

  if (!currentLesson || questions.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Lesson not found or no questions available.</p>
      </div>
    );
  }

  if (hearts <= 0 && !lessonComplete) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-xl p-8 shadow-lg text-center max-w-md">
          <div className="text-6xl mb-4">💔</div>
          <h2 className="text-2xl font-bold mb-4">You ran out of hearts!</h2>
          <p className="text-gray-600 mb-6">Don't worry, you can try again anytime.</p>
          <Button onClick={() => navigate(`/topic/${topicId}`)} className="w-full">
            Return to Topic
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm p-4">
        <div className="container mx-auto flex items-center justify-between">
          <button 
            onClick={() => navigate(`/topic/${topicId}`)}
            className="text-gray-500 hover:text-gray-700"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="m15 18-6-6 6-6"></path>
            </svg>
          </button>
          
          <div className="flex-1 mx-4">
            <Progress value={progress} className="h-3" />
          </div>
          
          <div className="flex items-center gap-2">
            {[...Array(3)].map((_, i) => (
              <Heart 
                key={i} 
                className={`w-6 h-6 ${i < hearts ? 'text-red-500 fill-red-500' : 'text-gray-300'}`} 
              />
            ))}
          </div>
        </div>
      </div>

      {/* Question Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          {currentQuestion && (
            <QuestionCard
              question={currentQuestion}
              selectedAnswer={selectedAnswer}
              onAnswerSelect={handleAnswerSelect}
              showFeedback={showFeedback}
              isCorrect={isCorrect}
            />
          )}
          
          <div className="mt-8 flex justify-center">
            <Button 
              onClick={handleAnswerSubmit}
              disabled={!selectedAnswer || showFeedback}
              className="w-full max-w-xs h-12 text-lg font-semibold"
              style={{ backgroundColor: selectedAnswer && !showFeedback ? '#3D99EC' : '' }}
            >
              {showFeedback ? (isCorrect ? 'Correct!' : 'Incorrect') : 'Check'}
            </Button>
          </div>
        </div>
      </div>

      {/* Result Modal */}
      {showResult && (
        <ResultModal
          score={score}
          totalQuestions={questions.length}
          xpEarned={currentLesson.xp}
          onContinue={handleContinue}
          isOpen={showResult}
        />
      )}
    </div>
  );
};

export default LessonPage;
