import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, ArrowLeft } from 'lucide-react';

export default function ComparisonFlow({ criteria, userName, onComplete }) {
  const navigate = useNavigate();

  // Generate all pairwise comparisons
  const generateComparisons = () => {
    const comparisons = [];
    for (let i = 0; i < criteria.length; i++) {
      for (let j = i + 1; j < criteria.length; j++) {
        comparisons.push({
          criterionA: criteria[i],
          criterionB: criteria[j],
          indexA: i,
          indexB: j,
        });
      }
    }
    return comparisons;
  };

  const [comparisons] = useState(generateComparisons());
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});

  const currentComparison = comparisons[currentIndex];
  const totalQuestions = comparisons.length;
  const progress = ((currentIndex + 1) / totalQuestions) * 100;

  // Get current answer or default to 0 (equal)
  const currentAnswer = answers[currentIndex] || 0;

  const handleSliderChange = (value) => {
    setAnswers({
      ...answers,
      [currentIndex]: value,
    });
  };

  const handleNext = () => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      // Finished - go to results
      onComplete(answers, comparisons);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const getImportanceText = () => {
    if (currentAnswer === 0) {
      return 'שווה';
    } else if (currentAnswer > 0) {
      return `← חשוב יותר`;
    } else {
      return `חשוב יותר →`;
    }
  };

  const getDetailedText = () => {
    const absValue = Math.abs(currentAnswer);
    if (currentAnswer === 0) {
      return 'שני הקריטריונים חשובים באותה מידה';
    } else if (currentAnswer > 0) {
      return `${currentComparison.criterionB} חשוב יותר (עוצמה: ${absValue})`;
    } else {
      return `${currentComparison.criterionA} חשוב יותר (עוצמה: ${absValue})`;
    }
  };

  // Calculate color based on importance (green = equal, red = most important)
  const getSliderColor = () => {
    const absValue = Math.abs(currentAnswer);
    const intensity = absValue / 8; // 0 to 1

    // Interpolate from green (0,128,0) to red (220,38,38)
    const r = Math.round(0 + intensity * 220);
    const g = Math.round(128 - intensity * 128);
    const b = Math.round(0 + intensity * 38);

    return `rgb(${r}, ${g}, ${b})`;
  };

  // Calculate slider background gradient
  const getSliderBackground = () => {
    const centerPercent = 50; // Center of slider
    const color = getSliderColor();
    const lightGray = '#e2e8f0';

    if (currentAnswer === 0) {
      // Equal - show minimal green in center
      return `linear-gradient(to right, ${lightGray} 0%, ${lightGray} 48%, ${color} 48%, ${color} 52%, ${lightGray} 52%, ${lightGray} 100%)`;
    } else if (currentAnswer < 0) {
      // Moving left - fill from center to left
      const fillPercent = centerPercent - ((currentAnswer + 8) / 16) * 50;
      return `linear-gradient(to right, ${color} 0%, ${color} ${fillPercent}%, ${lightGray} ${fillPercent}%, ${lightGray} 100%)`;
    } else {
      // Moving right - fill from center to right
      const fillPercent = centerPercent + (currentAnswer / 8) * 50;
      return `linear-gradient(to right, ${lightGray} 0%, ${lightGray} ${centerPercent}%, ${color} ${centerPercent}%, ${color} ${fillPercent}%, ${lightGray} ${fillPercent}%, ${lightGray} 100%)`;
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-slate-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header with user name */}
        {userName && (
          <div className="text-center mb-8">
            <p className="text-slate-600">
              מנהל: <span className="font-semibold text-slate-900">{userName}</span>
            </p>
          </div>
        )}

        {/* Main comparison card */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 mb-6">
          {/* Progress header */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-3">
              <span className="text-sm font-medium text-slate-900">
                {currentIndex + 1} מתוך {totalQuestions}
              </span>
              <span className="text-sm text-slate-500">התקדמות</span>
            </div>

            {/* Progress bar */}
            <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-slate-900 transition-all duration-300 ease-out"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Question section */}
          <div className="mb-8">
            <p className="text-center text-slate-500 text-sm mb-6">
              השוואה 1 מתוך {totalQuestions}
            </p>

            <h2 className="text-center text-2xl font-semibold text-slate-900 mb-8">
              Equal
            </h2>

            {/* Criteria comparison */}
            <div className="flex items-center justify-between gap-8 mb-8">
              {/* Left criterion */}
              <div className="flex-1 text-center">
                <div className="text-lg font-semibold text-slate-900">
                  {currentComparison.criterionA}
                </div>
              </div>

              {/* VS indicator */}
              <div className="text-slate-400 font-medium">
                מול
              </div>

              {/* Right criterion */}
              <div className="flex-1 text-center">
                <div className="text-lg font-semibold text-slate-900">
                  {currentComparison.criterionB}
                </div>
              </div>
            </div>

            {/* Slider */}
            <div className="mb-6">
              <div className="relative px-4">
                <input
                  type="range"
                  min="-8"
                  max="8"
                  value={currentAnswer}
                  onChange={(e) => handleSliderChange(parseInt(e.target.value))}
                  className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer slider"
                  style={{
                    background: getSliderBackground(),
                    '--thumb-color': getSliderColor()
                  }}
                />

                {/* Slider labels */}
                <div className="flex justify-between mt-2 text-xs text-slate-400">
                  <span>← חשוב יותר</span>
                  <span>שווה</span>
                  <span>חשוב יותר →</span>
                </div>
              </div>
            </div>

            {/* Explanation text */}
            <p className="text-center text-sm text-slate-600">
              {getDetailedText()}
            </p>
          </div>

          {/* Navigation buttons */}
          <div className="flex items-center justify-between gap-4">
            {/* Previous button */}
            <button
              onClick={handlePrevious}
              disabled={currentIndex === 0}
              className="flex items-center gap-2 px-6 py-3 bg-white border-2 border-slate-300 text-slate-700 font-medium rounded-xl hover:bg-slate-50 hover:border-slate-400 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>קודם</span>
            </button>

            {/* Next/Finish button */}
            <button
              onClick={handleNext}
              className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 transition-all shadow-sm"
            >
              <span>{currentIndex === totalQuestions - 1 ? 'סיים' : 'הבא'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Progress dots */}
        <div className="flex justify-center gap-2">
          {comparisons.map((_, index) => (
            <div
              key={index}
              className={`w-2 h-2 rounded-full transition-all ${
                index === currentIndex
                  ? 'bg-indigo-600 w-8'
                  : index < currentIndex
                  ? 'bg-slate-400'
                  : 'bg-slate-200'
              }`}
            />
          ))}
        </div>
      </div>

      <style>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: white;
          border: 3px solid var(--thumb-color, #1e293b);
          cursor: pointer;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .slider::-moz-range-thumb {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: white;
          border: 3px solid var(--thumb-color, #1e293b);
          cursor: pointer;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
      `}</style>
    </div>
  );
}
