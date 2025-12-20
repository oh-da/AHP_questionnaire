import { useLocation, useNavigate } from 'react-router-dom';
import { CheckCircle2, AlertCircle, BarChart3, Download, RotateCcw } from 'lucide-react';
import { calculateAHPWeights } from '../utils/ahpCalculator';
import { useEffect, useState } from 'react';

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const [results, setResults] = useState(null);

  useEffect(() => {
    if (location.state) {
      const { answers, comparisons, criteria, userName } = location.state;
      const calculatedResults = calculateAHPWeights(criteria, answers, comparisons);
      setResults({
        ...calculatedResults,
        userName,
        criteria
      });
    }
  }, [location.state]);

  if (!results) {
    return (
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center p-6">
        <div className="text-center">
          <p className="text-slate-600">אין תוצאות להצגה</p>
          <button
            onClick={() => navigate('/questionnaire')}
            className="mt-4 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            חזרה לשאלון
          </button>
        </div>
      </div>
    );
  }

  const sortedWeights = Object.entries(results.weights)
    .sort(([, a], [, b]) => b - a);

  const handleRestart = () => {
    navigate('/questionnaire');
  };

  const handleDownload = () => {
    const data = {
      userName: results.userName,
      criteria: results.criteria,
      weights: results.weights,
      consistency: {
        lambdaMax: results.lambdaMax,
        ci: results.ci,
        cr: results.cr,
        isConsistent: results.isConsistent
      }
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ahp-results.json';
    a.click();
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-slate-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-green-100 rounded-full">
              <CheckCircle2 className="w-8 h-8 text-green-600" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-slate-900 mb-2">
            תוצאות השאלון
          </h1>
          {results.userName && (
            <p className="text-slate-600">
              מנהל: <span className="font-semibold">{results.userName}</span>
            </p>
          )}
        </div>

        {/* Consistency Status */}
        <div className={`mb-6 p-6 rounded-2xl border-2 ${
          results.isConsistent
            ? 'bg-green-50 border-green-200'
            : 'bg-amber-50 border-amber-200'
        }`}>
          <div className="flex items-center gap-3 mb-3">
            {results.isConsistent ? (
              <CheckCircle2 className="w-6 h-6 text-green-600" />
            ) : (
              <AlertCircle className="w-6 h-6 text-amber-600" />
            )}
            <h2 className="text-xl font-semibold text-slate-900">
              {results.isConsistent ? 'התשובות עקביות!' : 'יש לבדוק עקביות'}
            </h2>
          </div>
          <div className="text-sm text-slate-600 space-y-1">
            <p>
              <span className="font-medium">יחס עקביות (CR):</span>{' '}
              {results.cr.toFixed(4)} {results.isConsistent ? '≤ 0.10' : '> 0.10'}
            </p>
            <p>
              <span className="font-medium">מדד עקביות (CI):</span>{' '}
              {results.ci.toFixed(4)}
            </p>
            <p>
              <span className="font-medium">Lambda Max:</span>{' '}
              {results.lambdaMax.toFixed(4)}
            </p>
          </div>
        </div>

        {/* Weights Visualization */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 mb-6">
          <div className="flex items-center gap-2 mb-6">
            <BarChart3 className="w-5 h-5 text-indigo-600" />
            <h2 className="text-2xl font-semibold text-slate-900">
              משקלי עדיפות
            </h2>
          </div>

          <div className="space-y-4">
            {sortedWeights.map(([criterion, weight], index) => (
              <div key={criterion}>
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium text-slate-900">{criterion}</span>
                  <div className="text-left">
                    <span className="text-sm text-slate-600 ml-2">
                      {(weight * 100).toFixed(2)}%
                    </span>
                    <span className="text-xs text-slate-400">
                      ({weight.toFixed(4)})
                    </span>
                  </div>
                </div>
                <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full transition-all duration-500 ${
                      index === 0
                        ? 'bg-indigo-600'
                        : index === 1
                        ? 'bg-indigo-500'
                        : 'bg-indigo-400'
                    }`}
                    style={{ width: `${weight * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4 justify-center">
          <button
            onClick={handleDownload}
            className="flex items-center gap-2 px-6 py-3 bg-white border-2 border-slate-300 text-slate-700 font-medium rounded-xl hover:bg-slate-50 hover:border-slate-400 transition-all"
          >
            <Download className="w-4 h-4" />
            <span>הורד תוצאות</span>
          </button>
          <button
            onClick={handleRestart}
            className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 transition-all shadow-sm"
          >
            <RotateCcw className="w-4 h-4" />
            <span>שאלון חדש</span>
          </button>
        </div>
      </div>
    </div>
  );
}
