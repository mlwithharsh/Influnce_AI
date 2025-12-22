import Layout from '@/components/Layout';
import { Card } from '@/components/ui/card';
import { useTheme } from '@/contexts/ThemeContext';
import { User, Mail, Calendar, MapPin, Link, Instagram, Twitter, Youtube, Edit, Camera } from 'lucide-react';

export default function Profile() {
  const { theme } = useTheme();

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Profile Header */}
        <Card className="p-6">
          <div className="flex items-center space-x-6">
            <div className="relative">
              <div className="w-24 h-24 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                <User className="w-12 h-12 text-white" />
              </div>
              <button className="absolute bottom-0 right-0 w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center hover:bg-blue-600 transition-colors">
                <Camera className="w-4 h-4 text-white" />
              </button>
            </div>
            <div className="flex-1">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>Sarah Johnson</h2>
                  <p className={theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}>@sarahj_lifestyle</p>
                </div>
                <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  <Edit className="w-4 h-4" />
                  <span>Edit Profile</span>
                </button>
              </div>
              <p className={`mt-3 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>Lifestyle influencer sharing daily inspiration, fashion tips, and wellness advice. Creating content that makes life more beautiful. ✨</p>
              <div className={`flex items-center space-x-6 mt-4 text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>
                <div className="flex items-center space-x-1">
                  <MapPin className="w-4 h-4" />
                  <span>Los Angeles, CA</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Link className="w-4 h-4" />
                  <a href="#" className={theme === 'dark' ? 'text-blue-400 hover:underline' : 'text-blue-600 hover:underline'}>sarahjohnson.com</a>
                </div>
                <div className="flex items-center space-x-1">
                  <Calendar className="w-4 h-4" />
                  <span>Joined March 2020</span>
                </div>
              </div>
            </div>
          </div>
        </Card>

        {/* Stats Overview */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="p-4 text-center">
            <div className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>2,147</div>
            <div className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Followers</div>
          </Card>
          <Card className="p-4 text-center">
            <div className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>892</div>
            <div className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Following</div>
          </Card>
          <Card className="p-4 text-center">
            <div className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>156</div>
            <div className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Posts</div>
          </Card>
          <Card className="p-4 text-center">
            <div className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>4.2%</div>
            <div className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Engagement</div>
          </Card>
        </div>

        {/* Account Settings */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="p-6">
            <h3 className={`text-lg font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-800'} mb-4`}>Account Information</h3>
            <div className="space-y-4">
              <div>
                <label className={`block text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'} mb-1`}>Full Name</label>
                <input 
                  type="text" 
                  defaultValue="Sarah Johnson" 
                  className={`w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    theme === 'dark' 
                      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                />
              </div>
              <div>
                <label className={`block text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'} mb-1`}>Username</label>
                <input 
                  type="text" 
                  defaultValue="@sarahj_lifestyle" 
                  className={`w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    theme === 'dark' 
                      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                />
              </div>
              <div>
                <label className={`block text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'} mb-1`}>Email</label>
                <div className="flex">
                  <input 
                    type="email" 
                    defaultValue="sarah@example.com" 
                    className={`flex-1 p-2 border rounded-l-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      theme === 'dark' 
                        ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
                        : 'bg-white border-gray-300 text-gray-900'
                    }`}
                  />
                  <button className="px-4 py-2 bg-blue-600 text-white rounded-r-lg hover:bg-blue-700 transition-colors">
                    Verify
                  </button>
                </div>
              </div>
              <div>
                <label className={`block text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'} mb-1`}>Bio</label>
                <textarea 
                  defaultValue="Lifestyle influencer sharing daily inspiration, fashion tips, and wellness advice." 
                  rows={3}
                  className={`w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    theme === 'dark' 
                      ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
                      : 'bg-white border-gray-300 text-gray-900'
                  }`}
                />
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <h3 className={`text-lg font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-800'} mb-4`}>Connected Accounts</h3>
            <div className="space-y-4">
              <div className={`flex items-center justify-between p-3 rounded-lg ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-50'}`}>
                <div className="flex items-center space-x-3">
                  <Instagram className="w-5 h-5 text-pink-600" />
                  <span className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>Instagram</span>
                </div>
                <span className="text-sm text-green-600">Connected</span>
              </div>
              <div className={`flex items-center justify-between p-3 rounded-lg ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-50'}`}>
                <div className="flex items-center space-x-3">
                  <Twitter className="w-5 h-5 text-blue-400" />
                  <span className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>Twitter</span>
                </div>
                <button className={`text-sm hover:underline ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`}>Connect</button>
              </div>
              <div className={`flex items-center justify-between p-3 rounded-lg ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-50'}`}>
                <div className="flex items-center space-x-3">
                  <Youtube className="w-5 h-5 text-red-600" />
                  <span className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>YouTube</span>
                </div>
                <button className={`text-sm hover:underline ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`}>Connect</button>
              </div>
            </div>
          </Card>
        </div>

        {/* Preferences */}
        <Card className="p-6">
          <h3 className={`text-lg font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-800'} mb-4`}>Preferences</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-800'} mb-3`}>Notifications</h4>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input type="checkbox" defaultChecked className="mr-2" />
                  <span className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>Email notifications</span>
                </label>
                <label className="flex items-center">
                  <input type="checkbox" defaultChecked className="mr-2" />
                  <span className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>Weekly analytics reports</span>
                </label>
                <label className="flex items-center">
                  <input type="checkbox" className="mr-2" />
                  <span className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>SMS notifications</span>
                </label>
              </div>
            </div>
            <div>
              <h4 className={`font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-800'} mb-3`}>Privacy</h4>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input type="checkbox" defaultChecked className="mr-2" />
                  <span className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>Make profile public</span>
                </label>
                <label className="flex items-center">
                  <input type="checkbox" className="mr-2" />
                  <span className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>Allow data sharing</span>
                </label>
                <label className="flex items-center">
                  <input type="checkbox" defaultChecked className="mr-2" />
                  <span className={`text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>Show analytics insights</span>
                </label>
              </div>
            </div>
          </div>
          <div className="mt-6 flex justify-end space-x-3">
            <button className={`px-4 py-2 border rounded-lg transition-colors ${
              theme === 'dark' 
                ? 'border-gray-600 text-gray-300 hover:bg-gray-700' 
                : 'border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}>
              Cancel
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Save Changes
            </button>
          </div>
        </Card>
      </div>
    </Layout>
  );
}