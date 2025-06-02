
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { useState } from 'react';

export interface Question {
  id: string;
  type: 'multiple-choice' | 'fill-blank' | 'true-false';
  question: string;
  options?: string[];
  correctAnswer: string;
  explanation: string;
}

interface QuestionCardProps {
  question: Question;
  selectedAnswer: string;
  onAnswerSelect: (answer: string) => void;
  showFeedback: boolean;
  isCorrect: boolean;
}

export function QuestionCard({ 
  question, 
  selectedAnswer, 
  onAnswerSelect, 
  showFeedback, 
  isCorrect 
}: QuestionCardProps) {
  const [fillBlankAnswer, setFillBlankAnswer] = useState('');

  const handleFillBlankChange = (value: string) => {
    setFillBlankAnswer(value);
    onAnswerSelect(value);
  };

  const renderQuestionContent = () => {
    switch (question.type) {
      case 'multiple-choice':
        return (
          <RadioGroup 
            value={selectedAnswer} 
            onValueChange={onAnswerSelect}
            disabled={showFeedback}
          >
            <div className="space-y-3">
              {question.options?.map((option, index) => {
                const optionId = `option-${index}`;
                const isSelected = selectedAnswer === option;
                const isCorrectOption = option === question.correctAnswer;
                
                let optionClass = "flex items-center space-x-3 p-4 rounded-lg border-2 cursor-pointer transition-colors ";
                
                if (showFeedback) {
                  if (isCorrectOption) {
                    optionClass += "border-green-500 bg-green-50 ";
                  } else if (isSelected && !isCorrectOption) {
                    optionClass += "border-red-500 bg-red-50 ";
                  } else {
                    optionClass += "border-gray-200 bg-gray-50 ";
                  }
                } else {
                  optionClass += isSelected 
                    ? "border-blue-500 bg-blue-50 " 
                    : "border-gray-200 hover:border-gray-300 ";
                }
                
                return (
                  <div key={index} className={optionClass}>
                    <RadioGroupItem value={option} id={optionId} />
                    <Label htmlFor={optionId} className="flex-1 cursor-pointer">
                      {option}
                    </Label>
                    {showFeedback && isCorrectOption && (
                      <div className="text-green-600">✓</div>
                    )}
                    {showFeedback && isSelected && !isCorrectOption && (
                      <div className="text-red-600">✗</div>
                    )}
                  </div>
                );
              })}
            </div>
          </RadioGroup>
        );

      case 'fill-blank':
        const parts = question.question.split('_____');
        return (
          <div className="space-y-4">
            <div className="text-lg">
              {parts[0]}
              <Input 
                value={fillBlankAnswer}
                onChange={(e) => handleFillBlankChange(e.target.value)}
                className={`inline-block w-48 mx-2 ${
                  showFeedback 
                    ? isCorrect 
                      ? 'border-green-500 bg-green-50' 
                      : 'border-red-500 bg-red-50'
                    : ''
                }`}
                placeholder="Type your answer..."
                disabled={showFeedback}
              />
              {parts[1]}
            </div>
            {showFeedback && (
              <div className={`p-3 rounded-lg ${isCorrect ? 'bg-green-50' : 'bg-red-50'}`}>
                <p className="font-medium">
                  {isCorrect ? '✓ Correct!' : '✗ Incorrect'}
                </p>
                <p className="text-sm mt-1">
                  The correct answer is: <strong>{question.correctAnswer}</strong>
                </p>
              </div>
            )}
          </div>
        );

      case 'true-false':
        return (
          <RadioGroup 
            value={selectedAnswer} 
            onValueChange={onAnswerSelect}
            disabled={showFeedback}
          >
            <div className="space-y-3">
              {['True', 'False'].map((option) => {
                const isSelected = selectedAnswer === option;
                const isCorrectOption = option === question.correctAnswer;
                
                let optionClass = "flex items-center space-x-3 p-4 rounded-lg border-2 cursor-pointer transition-colors ";
                
                if (showFeedback) {
                  if (isCorrectOption) {
                    optionClass += "border-green-500 bg-green-50 ";
                  } else if (isSelected && !isCorrectOption) {
                    optionClass += "border-red-500 bg-red-50 ";
                  } else {
                    optionClass += "border-gray-200 bg-gray-50 ";
                  }
                } else {
                  optionClass += isSelected 
                    ? "border-blue-500 bg-blue-50 " 
                    : "border-gray-200 hover:border-gray-300 ";
                }
                
                return (
                  <div key={option} className={optionClass}>
                    <RadioGroupItem value={option} id={option} />
                    <Label htmlFor={option} className="flex-1 cursor-pointer text-lg">
                      {option}
                    </Label>
                    {showFeedback && isCorrectOption && (
                      <div className="text-green-600 text-xl">✓</div>
                    )}
                    {showFeedback && isSelected && !isCorrectOption && (
                      <div className="text-red-600 text-xl">✗</div>
                    )}
                  </div>
                );
              })}
            </div>
          </RadioGroup>
        );

      default:
        return null;
    }
  };

  return (
    <div className="bg-white rounded-xl p-6 shadow-lg">
      <div className="mb-6">
        <h2 className="text-xl font-bold mb-4">{question.question}</h2>
        {renderQuestionContent()}
      </div>
      
      {showFeedback && (
        <div className={`mt-6 p-4 rounded-lg ${
          isCorrect ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
        }`}>
          <div className="flex items-center mb-2">
            <div className={`w-6 h-6 rounded-full flex items-center justify-center mr-3 ${
              isCorrect ? 'bg-green-500' : 'bg-red-500'
            }`}>
              <span className="text-white text-sm font-bold">
                {isCorrect ? '✓' : '✗'}
              </span>
            </div>
            <span className={`font-semibold ${
              isCorrect ? 'text-green-800' : 'text-red-800'
            }`}>
              {isCorrect ? 'Great job!' : 'Not quite right'}
            </span>
          </div>
          <p className={`text-sm ${
            isCorrect ? 'text-green-700' : 'text-red-700'
          }`}>
            {question.explanation}
          </p>
        </div>
      )}
    </div>
  );
}
