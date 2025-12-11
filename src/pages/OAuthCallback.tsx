import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import { Loader2 } from 'lucide-react';

export default function OAuthCallback() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const { setToken, fetchConnectedAccounts } = useAuthStore();
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    useEffect(() => {
        const handleCallback = async () => {
            const code = searchParams.get('code');
            const platform = window.location.pathname.split('/')[2]; // Extract platform from URL

            if (!code) {
                navigate('/dashboard?error=no_code');
                return;
            }

            try {
                // Call backend OAuth callback to exchange code for tokens
                const res = await fetch(`${API_URL}/auth/${platform}/callback?code=${encodeURIComponent(code)}`);
                if (!res.ok) throw new Error('OAuth callback failed');

                const data = await res.json();
                if (data?.access_token) {
                    setToken(data.access_token);
                }

                await fetchConnectedAccounts();
                navigate('/dashboard?success=connected');
            } catch (error) {
                console.error('OAuth callback error:', error);
                navigate('/dashboard?error=connection_failed');
            }
        };

        handleCallback();
    }, [searchParams, navigate, setToken, fetchConnectedAccounts]);

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center">
            <div className="text-center">
                <Loader2 className="w-16 h-16 text-white animate-spin mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-white mb-2">Connecting your account...</h2>
                <p className="text-purple-200">Please wait while we complete the connection.</p>
            </div>
        </div>
    );
}
