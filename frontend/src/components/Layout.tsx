import { ReactNode } from 'react';
import { MessageCircle, Home, BarChart3, User, Settings, Sun, Moon } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { useTheme } from '@/contexts/ThemeContext';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();

  const navItems = [
    { icon: Home, label: 'Home', path: '/' },
    { icon: MessageCircle, label: 'AI Assistant', path: '/ai-chat' },
    { icon: BarChart3, label: 'Analytics', path: '/analytics' },
    { icon: User, label: 'Profile', path: '/profile' },
    { icon: Settings, label: 'Settings', path: '/settings' },
  ];

  return (
    <div className={cn(
      "min-h-screen flex",
      theme === 'dark' 
        ? 'bg-gray-900 text-white' 
        : 'bg-gray-50 text-gray-900'
    )}>
      {/* Sidebar Navigation */}
      <div className={cn(
        "w-64 shadow-lg",
        theme === 'dark' 
          ? 'bg-gray-800 border-r border-gray-700' 
          : 'bg-white'
      )}>
        <div className="p-6">
          <div className="flex items-center justify-between mb-8">
            <h1 className={cn(
              "text-2xl font-bold",
              theme === 'dark' ? 'text-white' : 'text-gray-800'
            )}>
              Influence AI
            </h1>
            <button
              onClick={toggleTheme}
              className={cn(
                "p-2 rounded-lg transition-colors",
                theme === 'dark'
                  ? 'bg-gray-700 hover:bg-gray-600 text-yellow-400'
                  : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
              )}
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
            </button>
          </div>
          <nav className="space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={cn(
                    'flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors',
                    isActive
                      ? (theme === 'dark'
                          ? 'bg-blue-900 text-blue-300'
                          : 'bg-blue-100 text-blue-700')
                      : (theme === 'dark'
                          ? 'text-gray-300 hover:bg-gray-700'
                          : 'text-gray-600 hover:bg-gray-100')
                  )}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className={cn(
          "shadow-sm border-b",
          theme === 'dark'
            ? 'bg-gray-800 border-gray-700'
            : 'bg-white border-gray-200'
        )}>
          <div className="px-6 py-4 flex items-center justify-between">
            <h2 className={cn(
              "text-xl font-semibold",
              theme === 'dark' ? 'text-white' : 'text-gray-800'
            )}>
              {location.pathname === '/' && 'Dashboard'}
              {location.pathname === '/ai-chat' && 'AI Assistant'}
              {location.pathname === '/analytics' && 'Analytics'}
              {location.pathname === '/profile' && 'Profile'}
              {location.pathname === '/settings' && 'Settings'}
            </h2>
            <div className="flex items-center space-x-4">
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">U</span>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}