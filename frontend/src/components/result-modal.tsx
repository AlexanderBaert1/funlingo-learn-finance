
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Trophy, Star } from 'lucide-react';

interface ResultModalProps {
  score: number;
  totalQuestions: number;
  xpEarned: number;
  onContinue: () => void;
  isOpen: boolean;
}

export function ResultModal({ 
  score, 
  totalQuestions, 
  xpEarned, 
  onContinue, 
  isOpen 
}: ResultModalProps) {
  const correctAnswers = score / 10; // 10 points per correct answer
  const percentage = Math.round((correctAnswers / totalQuestions) * 100);
  
  const getResultMessage = () => {
    if (percentage >= 90) return "Outstanding!";
    if (percentage >= 80) return "Great job!";
    if (percentage >= 70) return "Good work!";
    if (percentage >= 60) return "Not bad!";
    return "Keep practicing!";
  };

  const getResultIcon = () => {
    if (percentage >= 80) return <Trophy className="w-16 h-16 text-yellow-500" />;
    return <Star className="w-16 h-16 text-blue-500" />;
  };

  return (
    <Dialog open={isOpen}>
      <DialogContent className="max-w-md">
        <div className="text-center py-6">
          <div className="mb-6">
            {getResultIcon()}
          </div>
          
          <h2 className="text-2xl font-bold mb-2">{getResultMessage()}</h2>
          
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-600">Correct answers:</span>
              <span className="font-semibold">{correctAnswers}/{totalQuestions}</span>
            </div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-600">Accuracy:</span>
              <span className="font-semibold">{percentage}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">XP earned:</span>
              <span className="font-semibold text-green-600">+{xpEarned}</span>
            </div>
          </div>
          
          <Button 
            onClick={onContinue}
            className="w-full h-12 text-lg font-semibold"
            style={{ backgroundColor: '#3D99EC' }}
          >
            Continue
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
