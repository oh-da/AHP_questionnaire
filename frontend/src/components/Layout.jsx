import { Outlet, Link } from 'react-router-dom';
import { Scale, BarChart3, ClipboardList } from 'lucide-react';
import { cn } from '../utils/cn';

export default function Layout() {
  const navItems = [
    { name: 'questionnaire', label: 'שאלון', icon: ClipboardList, path: '/questionnaire' },
    { name: 'results', label: 'תוצאות', icon: BarChart3, path: '/results' },
  ];

  return (
    <div className="min-h-screen bg-slate-50" dir="rtl">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link
              to="/questionnaire"
              className="flex items-center gap-3 hover:opacity-80 transition-opacity"
            >
              <div className="p-2 bg-indigo-100 rounded-xl">
                <Scale className="w-5 h-5 text-indigo-600" />
              </div>
              <span className="font-semibold text-slate-800 tracking-tight">
                כלי AHP
              </span>
            </Link>

            {/* Navigation */}
            <nav className="flex items-center gap-3">
              <div className="flex items-center gap-1">
                {navItems.map((item) => {
                  const Icon = item.icon;

                  return (
                    <Link
                      key={item.name}
                      to={item.path}
                      className={cn(
                        "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all",
                        "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                      )}
                    >
                      <span className="hidden sm:inline">{item.label}</span>
                      <Icon className="w-4 h-4" />
                    </Link>
                  );
                })}
              </div>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main>
        <Outlet />
      </main>
    </div>
  );
}
