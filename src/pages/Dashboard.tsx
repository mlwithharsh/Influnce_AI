import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import {
    Instagram,
    Twitter,
    Youtube,
    TrendingUp,
    Users,
    Heart,
    MessageCircle,
    Eye,
    BarChart3,
    Calendar,
    Sparkles,
    LogOut,
    Settings as SettingsIcon,
} from 'lucide-react';

interface PlatformStats {
    platform: string;
    followers: number;
    engagement: number;
    posts: number;
    growth: number;
}

export default function Dashboard() {
    const { user, isAuthenticated, connectedAccounts, logout, fetchConnectedAccounts, connectPlatform } = useAuthStore();
    const navigate = useNavigate();
    const [stats, setStats] = useState<PlatformStats[]>([]);

    useEffect(() => {
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }
        fetchConnectedAccounts();
    }, [isAuthenticated, navigate, fetchConnectedAccounts]);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const isConnected = (platform: string) => {
        return connectedAccounts.some((acc) => acc.platform === platform && acc.connected);
    };

    const getPlatformIcon = (platform: string) => {
        switch (platform) {
            case 'instagram':
                return <Instagram className="w-6 h-6" />;
            case 'twitter':
                return <Twitter className="w-6 h-6" />;
            case 'youtube':
                return <Youtube className="w-6 h-6" />;
            default:
                return null;
        }
    };

    const getPlatformColor = (platform: string) => {
        switch (platform) {
            case 'instagram':
                return 'from-purple-500 to-pink-500';
            case 'twitter':
                return 'from-blue-400 to-cyan-500';
            case 'youtube':
                return 'from-red-500 to-orange-500';
            default:
                return 'from-gray-500 to-gray-600';
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            {/* Header */}
            <header className="bg-white/10 backdrop-blur-lg border-b border-white/10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                                <Sparkles className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-white">InfluenceAI</h1>
                                <p className="text-sm text-purple-200">Welcome back, {user?.username}!</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <button
                                onClick={() => navigate('/settings')}
                                className="p-2 text-white hover:bg-white/10 rounded-lg transition-colors"
                            >
                                <SettingsIcon className="w-5 h-5" />
                            </button>
                            <button
                                onClick={handleLogout}
                                className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors"
                            >
                                <LogOut className="w-4 h-4" />
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Connect Accounts Section */}
                <div className="mb-8">
                    <h2 className="text-2xl font-bold text-white mb-4">Connect Your Accounts</h2>
                    <div className="grid md:grid-cols-3 gap-4">
                        {['instagram', 'twitter', 'youtube'].map((platform) => {
                            const connected = isConnected(platform);
                            return (
                                <button
                                    key={platform}
                                    onClick={() => !connected && connectPlatform(platform as any)}
                                    className={`p-6 rounded-2xl border-2 transition-all ${connected
                                            ? 'bg-white/20 border-white/30 cursor-default'
                                            : 'bg-white/5 border-white/10 hover:bg-white/10 hover:border-white/20'
                                        }`}
                                >
                                    <div className="flex items-center justify-between mb-4">
                                        <div className={`w-12 h-12 bg-gradient-to-br ${getPlatformColor(platform)} rounded-xl flex items-center justify-center text-white`}>
                                            {getPlatformIcon(platform)}
                                        </div>
                                        {connected && (
                                            <span className="px-3 py-1 bg-green-500/20 text-green-300 text-xs font-semibold rounded-full border border-green-500/30">
                                                Connected
                                            </span>
                                        )}
                                    </div>
                                    <h3 className="text-lg font-semibold text-white capitalize mb-1">
                                        {platform}
                                    </h3>
                                    <p className="text-sm text-purple-200">
                                        {connected ? 'Account connected' : 'Click to connect'}
                                    </p>
                                </button>
                            );
                        })}
                    </div>
                </div>

                {/* Stats Overview */}
                <div className="grid md:grid-cols-4 gap-4 mb-8">
                    <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 backdrop-blur-lg rounded-2xl p-6 border border-white/10">
                        <div className="flex items-center justify-between mb-4">
                            <div className="w-12 h-12 bg-purple-500/30 rounded-xl flex items-center justify-center">
                                <Users className="w-6 h-6 text-purple-300" />
                            </div>
                            <span className="text-green-400 text-sm font-semibold">+12.5%</span>
                        </div>
                        <h3 className="text-3xl font-bold text-white mb-1">24.5K</h3>
                        <p className="text-purple-200 text-sm">Total Followers</p>
                    </div>

                    <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 backdrop-blur-lg rounded-2xl p-6 border border-white/10">
                        <div className="flex items-center justify-between mb-4">
                            <div className="w-12 h-12 bg-blue-500/30 rounded-xl flex items-center justify-center">
                                <Heart className="w-6 h-6 text-blue-300" />
                            </div>
                            <span className="text-green-400 text-sm font-semibold">+8.2%</span>
                        </div>
                        <h3 className="text-3xl font-bold text-white mb-1">4.8%</h3>
                        <p className="text-blue-200 text-sm">Engagement Rate</p>
                    </div>

                    <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 backdrop-blur-lg rounded-2xl p-6 border border-white/10">
                        <div className="flex items-center justify-between mb-4">
                            <div className="w-12 h-12 bg-green-500/30 rounded-xl flex items-center justify-center">
                                <TrendingUp className="w-6 h-6 text-green-300" />
                            </div>
                            <span className="text-green-400 text-sm font-semibold">+15.3%</span>
                        </div>
                        <h3 className="text-3xl font-bold text-white mb-1">156</h3>
                        <p className="text-green-200 text-sm">Total Posts</p>
                    </div>

                    <div className="bg-gradient-to-br from-orange-500/20 to-red-500/20 backdrop-blur-lg rounded-2xl p-6 border border-white/10">
                        <div className="flex items-center justify-between mb-4">
                            <div className="w-12 h-12 bg-orange-500/30 rounded-xl flex items-center justify-center">
                                <Eye className="w-6 h-6 text-orange-300" />
                            </div>
                            <span className="text-green-400 text-sm font-semibold">+22.1%</span>
                        </div>
                        <h3 className="text-3xl font-bold text-white mb-1">1.2M</h3>
                        <p className="text-orange-200 text-sm">Total Reach</p>
                    </div>
                </div>

                {/* Recent Activity */}
                <div className="grid lg:grid-cols-2 gap-8">
                    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/10">
                        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                            <BarChart3 className="w-5 h-5" />
                            Platform Performance
                        </h3>
                        <div className="space-y-4">
                            {connectedAccounts.map((account) => (
                                <div key={account.platform} className="flex items-center justify-between p-4 bg-white/5 rounded-xl">
                                    <div className="flex items-center gap-3">
                                        <div className={`w-10 h-10 bg-gradient-to-br ${getPlatformColor(account.platform)} rounded-lg flex items-center justify-center text-white`}>
                                            {getPlatformIcon(account.platform)}
                                        </div>
                                        <div>
                                            <p className="font-semibold text-white capitalize">{account.platform}</p>
                                            <p className="text-sm text-purple-200">ID: {account.account_id}</p>
                                        </div>
                                    </div>
                                    <button className="px-4 py-2 bg-purple-500/20 hover:bg-purple-500/30 text-purple-200 rounded-lg text-sm font-medium transition-colors">
                                        View Analytics
                                    </button>
                                </div>
                            ))}
                            {connectedAccounts.length === 0 && (
                                <p className="text-center text-purple-200 py-8">
                                    No accounts connected yet. Connect your social media accounts to see analytics.
                                </p>
                            )}
                        </div>
                    </div>

                    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/10">
                        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                            <Calendar className="w-5 h-5" />
                            AI Recommendations
                        </h3>
                        <div className="space-y-3">
                            <div className="p-4 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl border border-purple-500/30">
                                <div className="flex items-start gap-3">
                                    <Sparkles className="w-5 h-5 text-purple-300 flex-shrink-0 mt-0.5" />
                                    <div>
                                        <p className="font-semibold text-white mb-1">Best Time to Post</p>
                                        <p className="text-sm text-purple-200">
                                            Tuesday at 3:00 PM has 45% higher engagement
                                        </p>
                                    </div>
                                </div>
                            </div>
                            <div className="p-4 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-xl border border-blue-500/30">
                                <div className="flex items-start gap-3">
                                    <TrendingUp className="w-5 h-5 text-blue-300 flex-shrink-0 mt-0.5" />
                                    <div>
                                        <p className="font-semibold text-white mb-1">Trending Topic</p>
                                        <p className="text-sm text-blue-200">
                                            #TechInnovation is trending in your niche
                                        </p>
                                    </div>
                                </div>
                            </div>
                            <div className="p-4 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl border border-green-500/30">
                                <div className="flex items-start gap-3">
                                    <MessageCircle className="w-5 h-5 text-green-300 flex-shrink-0 mt-0.5" />
                                    <div>
                                        <p className="font-semibold text-white mb-1">Content Suggestion</p>
                                        <p className="text-sm text-green-200">
                                            Video content gets 3x more engagement
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
