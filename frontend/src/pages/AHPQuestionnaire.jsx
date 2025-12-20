import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Settings, ArrowRight } from 'lucide-react';

// Default criteria from the Python app
const DEFAULT_CRITERIA = [
  'Passenger Activity',
  'Service & Modes',
  'Location',
  'Population & Jobs',
  'Bus Terminal'
];

export default function AHPQuestionnaire() {
  const navigate = useNavigate();
  const [name, setName] = useState('Ohad Dahan');
  const [criteria, setCriteria] = useState(DEFAULT_CRITERIA);
  const [showSettings, setShowSettings] = useState(false);

  // Calculate number of pairwise comparisons: n(n-1)/2
  const numComparisons = (criteria.length * (criteria.length - 1)) / 2;

  const handleStart = () => {
    // TODO: Navigate to comparison flow
    console.log('Starting questionnaire with:', { name, criteria });
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center p-6">
      <div className="w-full max-w-2xl">
        {/* Header Section */}
        <div className="text-center mb-8">
          {/* Icon */}
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-indigo-100 rounded-2xl">
              <Sparkles className="w-8 h-8 text-indigo-600" />
            </div>
          </div>

          {/* Title */}
          <h1 className="text-4xl font-bold text-slate-900 mb-4">
            שאלון AHP
          </h1>

          {/* Subtitle */}
          <p className="text-slate-600 text-lg leading-relaxed max-w-xl mx-auto">
            תנדוד קריטריונים באמצעות תהליך האירלוכיה האנליטית דרך השואלות זוגית
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
          {/* Name Field */}
          <div className="mb-6">
            <label className="block text-sm text-slate-600 mb-2">
              שמך (אופציונלי)
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              placeholder="הכנס את שמך"
            />
          </div>

          {/* Criteria Section */}
          <div className="mb-6">
            <label className="block text-sm text-slate-600 mb-3">
              קריטריונים להשוואה:
            </label>

            {/* Criteria Tags */}
            <div className="flex flex-wrap gap-2 mb-4">
              {criteria.map((criterion, index) => (
                <span
                  key={index}
                  className="px-4 py-2 bg-slate-100 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-200 transition-colors"
                >
                  {criterion}
                </span>
              ))}
            </div>

            {/* Comparison Count */}
            <p className="text-slate-500 text-sm">
              תצטרך {numComparisons} השוואות זוגיות
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            {/* Settings Button */}
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-white border-2 border-slate-300 text-slate-700 font-medium rounded-xl hover:bg-slate-50 hover:border-slate-400 transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-400"
            >
              <Settings className="w-4 h-4" />
              <span>הגדרות</span>
            </button>

            {/* Start Button */}
            <button
              onClick={handleStart}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-sm"
            >
              <span>התחל</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Settings Panel (if shown) */}
        {showSettings && (
          <div className="mt-6 bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">
              הגדרות
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-slate-600 mb-2">
                  ערוך קריטריונים (אחד בכל שורה)
                </label>
                <textarea
                  value={criteria.join('\n')}
                  onChange={(e) => {
                    const newCriteria = e.target.value
                      .split('\n')
                      .map(c => c.trim())
                      .filter(c => c.length > 0);
                    if (newCriteria.length >= 2) {
                      setCriteria(newCriteria);
                    }
                  }}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all font-mono text-sm"
                  rows={6}
                  placeholder="הכנס קריטריונים..."
                />
                <p className="mt-2 text-xs text-slate-500">
                  נדרשים לפחות 2 קריטריונים
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
