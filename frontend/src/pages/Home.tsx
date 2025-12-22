import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { MessageCircle, TrendingUp, Users, Heart, Eye, Share2 } from 'lucide-react';
import { useState } from 'react';
import { useTheme } from '@/contexts/ThemeContext';
import { cn } from '@/lib/utils';

interface Post {
  id: string;
  image: string;
  caption: string;
  likes: number;
  comments: number;
  views: number;
  timestamp: string;
  engagement: number;
}

interface AIInsight {
  id: string;
  title: string;
  description: string;
  type: 'trending' | 'engagement' | 'optimal_time';
  impact: 'high' | 'medium' | 'low';
}

export default function Home() {
  const { theme } = useTheme();
  
  const [posts] = useState<Post[]>([
    {
      id: '1',
      image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=modern%20lifestyle%20photo%20with%20bright%20colors%20and%20engaging%20composition&image_size=square',
      caption: 'New collection launch! 🚀 Excited to share these amazing pieces with you all. Link in bio! #fashion #lifestyle #newcollection',
      likes: 1247,
      comments: 89,
      views: 5420,
      timestamp: '2 hours ago',
      engagement: 24.5
    },
    {
      id: '2',
      image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=cozy%20coffee%20shop%20aesthetic%20with%20warm%20lighting%20and%20minimalist%20style&image_size=square',
      caption: 'Morning coffee vibes ☕ Perfect start to a productive day! What\'s your morning routine?',
      likes: 892,
      comments: 156,
      views: 3210,
      timestamp: '5 hours ago',
      engagement: 32.1
    }
  ]);

  const [aiInsights] = useState<AIInsight[]>([
    {
      id: '1',
      title: 'Best Posting Time',
      description: 'Your audience is most active between 6-8 PM. Posting during this window could increase engagement by 35%.',
      type: 'optimal_time',
      impact: 'high'
    },
    {
      id: '2',
      title: 'Trending Hashtag',
      description: '#lifestyle is trending in your niche. Consider incorporating it in your next 3 posts.',
      type: 'trending',
      impact: 'medium'
    },
    {
      id: '3',
      title: 'Engagement Boost',
      description: 'Posts with questions get 45% more comments. Try ending captions with engaging questions.',
      type: 'engagement',
      impact: 'high'
    }
  ]);

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'trending': return <TrendingUp className="w-5 h-5" />;
      case 'engagement': return <Users className="w-5 h-5" />;
      case 'optimal_time': return <MessageCircle className="w-5 h-5" />;
      default: return <MessageCircle className="w-5 h-5" />;
    }
  };

  return (
    <Layout>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Instagram-style Feed */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h3 className={cn(
              "text-lg font-semibold",
              theme === 'dark' ? 'text-white' : 'text-gray-800'
            )}>
              Recent Posts
            </h3>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Create Post
            </button>
          </div>

          {posts.map((post) => (
            <Card key={post.id} className="rounded-xl shadow-sm border-0 overflow-hidden">
              {/* Post Header */}
              <div className="p-4 flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-semibold">U</span>
                </div>
                <div>
                  <p className={cn(
                    "font-semibold",
                    theme === 'dark' ? 'text-white' : 'text-gray-800'
                  )}>
                    username
                  </p>
                  <p className={cn(
                    "text-sm",
                    theme === 'dark' ? 'text-gray-400' : 'text-gray-500'
                  )}>
                    {post.timestamp}
                  </p>
                </div>
              </div>

              {/* Post Image */}
              <div className="aspect-square bg-gray-100 dark:bg-gray-700">
                <img 
                  src={post.image} 
                  alt="Post content"
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Post Actions */}
              <div className="p-4">
                <div className="flex items-center space-x-4 mb-3">
                  <button className="flex items-center space-x-1 text-gray-600 hover:text-red-500 transition-colors">
                    <Heart className="w-5 h-5" />
                    <span className="text-sm">{post.likes}</span>
                  </button>
                  <button className="flex items-center space-x-1 text-gray-600 hover:text-blue-500 transition-colors">
                    <MessageCircle className="w-5 h-5" />
                    <span className="text-sm">{post.comments}</span>
                  </button>
                  <button className="flex items-center space-x-1 text-gray-600 hover:text-green-500 transition-colors">
                    <Share2 className="w-5 h-5" />
                  </button>
                  <button className="flex items-center space-x-1 text-gray-600 hover:text-purple-500 transition-colors ml-auto">
                    <Eye className="w-5 h-5" />
                    <span className="text-sm">{post.views}</span>
                  </button>
                </div>
                
                {/* Caption */}
                <p className={cn(
                  "text-sm leading-relaxed",
                  theme === 'dark' ? 'text-gray-300' : 'text-gray-800'
                )}>
                  {post.caption}
                </p>
                
                {/* Engagement Rate */}
                <div className="mt-3 pt-3 border-t border-gray-100 dark:border-gray-700">
                  <div className="flex items-center justify-between text-sm">
                    <span className={cn(
                      "text-gray-500",
                      theme === 'dark' ? 'dark:text-gray-400' : ''
                    )}>
                      Engagement Rate
                    </span>
                    <span className="font-semibold text-green-600">{post.engagement}%</span>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* AI Insights Sidebar */}
        <div className="space-y-6">
          <Card className="rounded-xl shadow-sm border-0 p-6">
            <h3 className={cn(
              "text-lg font-semibold mb-4 flex items-center",
              theme === 'dark' ? 'text-white' : 'text-gray-800'
            )}>
              <MessageCircle className="w-5 h-5 mr-2 text-blue-600" />
              AI Insights
            </h3>
            <div className="space-y-4">
              {aiInsights.map((insight) => (
                <div key={insight.id} className={cn(
                  "p-4 rounded-lg border",
                  theme === 'dark'
                    ? 'bg-blue-900 border-blue-800'
                    : 'bg-blue-50 border-blue-100'
                )}>
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      {getTypeIcon(insight.type)}
                      <h4 className={cn(
                        "font-medium",
                        theme === 'dark' ? 'text-white' : 'text-gray-800'
                      )}>
                        {insight.title}
                      </h4>
                    </div>
                    <span className={cn(
                      "px-2 py-1 rounded-full text-xs font-medium",
                      getImpactColor(insight.impact)
                    )}>
                      {insight.impact}
                    </span>
                  </div>
                  <p className={cn(
                    "text-sm leading-relaxed",
                    theme === 'dark' ? 'text-gray-300' : 'text-gray-600'
                  )}>
                    {insight.description}
                  </p>
                </div>
              ))}
            </div>
          </Card>

          {/* Quick Stats */}
          <Card className="rounded-xl shadow-sm border-0 p-6">
            <h3 className={cn(
              "text-lg font-semibold mb-4",
              theme === 'dark' ? 'text-white' : 'text-gray-800'
            )}>
              Quick Stats
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div className={cn(
                "text-center p-3 rounded-lg",
                theme === 'dark' ? 'bg-purple-900' : 'bg-purple-50'
              )}>
                <div className="text-2xl font-bold text-purple-600">2.1K</div>
                <div className={cn(
                  "text-sm",
                  theme === 'dark' ? 'text-gray-300' : 'text-gray-600'
                )}>
                  Followers
                </div>
              </div>
              <div className={cn(
                "text-center p-3 rounded-lg",
                theme === 'dark' ? 'bg-green-900' : 'bg-green-50'
              )}>
                <div className="text-2xl font-bold text-green-600">4.8%</div>
                <div className={cn(
                  "text-sm",
                  theme === 'dark' ? 'text-gray-300' : 'text-gray-600'
                )}>
                  Avg. Engagement
                </div>
              </div>
              <div className={cn(
                "text-center p-3 rounded-lg",
                theme === 'dark' ? 'bg-blue-900' : 'bg-blue-50'
              )}>
                <div className="text-2xl font-bold text-blue-600">156</div>
                <div className={cn(
                  "text-sm",
                  theme === 'dark' ? 'text-gray-300' : 'text-gray-600'
                )}>
                  Posts This Month
                </div>
              </div>
              <div className={cn(
                "text-center p-3 rounded-lg",
                theme === 'dark' ? 'bg-orange-900' : 'bg-orange-50'
              )}>
                <div className="text-2xl font-bold text-orange-600">+23%</div>
                <div className={cn(
                  "text-sm",
                  theme === 'dark' ? 'text-gray-300' : 'text-gray-600'
                )}>
                  Growth Rate
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </Layout>
  );
}