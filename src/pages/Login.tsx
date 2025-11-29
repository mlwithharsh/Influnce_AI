import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import { Instagram, Twitter, Youtube, Sparkles, TrendingUp, BarChart3 } from 'lucide-react';

export default function Login() {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login, register } = useAuthStore();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (isLogin) {
                await login(email, password);
            } else {
                await register(username, email, password);
            }
            navigate('/dashboard');
        } catch (err) {
            setError(isLogin ? 'Invalid credentials' : 'Registration failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
            {/* Animated background */}
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-purple-500/20 to-transparent rounded-full blur-3xl animate-pulse"></div>
                <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-blue-500/20 to-transparent rounded-full blur-3xl animate-pulse delay-1000"></div>
            </div>

            <div className="relative w-full max-w-6xl grid lg:grid-cols-2 gap-8 items-center">
                {/* Left side - Branding */}
                <div className="hidden lg:block text-white space-y-8">
                    <div className="space-y-4">
                        <div className="flex items-center gap-3">
                            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                                <Sparkles className="w-7 h-7" />
                            </div>
                            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">
                                InfluenceAI
                            </h1>
                        </div>
                        <p className="text-xl text-purple-200">
                            Supercharge your social media presence with AI-powered insights
                        </p>
                    </div>

                    <div className="space-y-6">
                        <div className="flex items-start gap-4 bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
                            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center flex-shrink-0">
                                <TrendingUp className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-lg mb-1">Real-time Analytics</h3>
                                <p className="text-purple-200 text-sm">
                                    Track your performance across Instagram, Twitter, and YouTube in one place
                                </p>
                            </div>
                        </div>

                        <div className="flex items-start gap-4 bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
                            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center flex-shrink-0">
                                <Sparkles className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-lg mb-1">AI-Powered Insights</h3>
                                <p className="text-purple-200 text-sm">
                                    Get personalized recommendations to optimize your content strategy
                                </p>
                            </div>
                        </div>

                        <div className="flex items-start gap-4 bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
                            <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center flex-shrink-0">
                                <BarChart3 className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-lg mb-1">Trend Predictions</h3>
                                <p className="text-purple-200 text-sm">
                                    Stay ahead with AI predictions on trending topics and optimal posting times
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right side - Login/Register Form */}
                <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/20">
                    <div className="mb-8">
                        <h2 className="text-3xl font-bold text-gray-900 mb-2">
                            {isLogin ? 'Welcome Back' : 'Create Account'}
                        </h2>
                        <p className="text-gray-600">
                            {isLogin
                                ? 'Sign in to access your analytics dashboard'
                                : 'Start your journey to social media success'}
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {!isLogin && (
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Username
                                </label>
                                <input
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                                    placeholder="johndoe"
                                    required={!isLogin}
                                />
                            </div>
                        )}

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Email
                            </label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                                placeholder="you@example.com"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Password
                            </label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                                placeholder="••••••••"
                                required
                            />
                        </div>

                        {error && (
                            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                        >
                            {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Create Account'}
                        </button>
                    </form>

                    <div className="mt-6">
                        <button
                            onClick={() => {
                                setIsLogin(!isLogin);
                                setError('');
                            }}
                            className="w-full text-center text-sm text-gray-600 hover:text-purple-600 transition-colors"
                        >
                            {isLogin ? "Don't have an account? " : 'Already have an account? '}
                            <span className="font-semibold text-purple-600">
                                {isLogin ? 'Sign Up' : 'Sign In'}
                            </span>
                        </button>
                    </div>

                    <div className="mt-8 pt-8 border-t border-gray-200">
                        <p className="text-center text-sm text-gray-600 mb-4">
                            Connect with your social accounts
                        </p>
                        <div className="grid grid-cols-3 gap-3">
                            <button className="flex items-center justify-center gap-2 px-4 py-3 border border-gray-300 rounded-xl hover:bg-gradient-to-br hover:from-purple-50 hover:to-pink-50 hover:border-purple-300 transition-all group">
                                <Instagram className="w-5 h-5 text-pink-600 group-hover:scale-110 transition-transform" />
                            </button>
                            <button className="flex items-center justify-center gap-2 px-4 py-3 border border-gray-300 rounded-xl hover:bg-gradient-to-br hover:from-blue-50 hover:to-cyan-50 hover:border-blue-300 transition-all group">
                                <Twitter className="w-5 h-5 text-blue-500 group-hover:scale-110 transition-transform" />
                            </button>
                            <button className="flex items-center justify-center gap-2 px-4 py-3 border border-gray-300 rounded-xl hover:bg-gradient-to-br hover:from-red-50 hover:to-orange-50 hover:border-red-300 transition-all group">
                                <Youtube className="w-5 h-5 text-red-600 group-hover:scale-110 transition-transform" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
