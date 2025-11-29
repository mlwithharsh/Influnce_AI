/**
 * Authentication Store
 * 
 * This Zustand store manages all authentication state for the application.
 * It handles user login, registration, OAuth connections, and session persistence.
 * 
 * Features:
 * - User authentication with JWT tokens
 * - Persistent sessions (survives page refresh)
 * - Connected social accounts tracking
 * - OAuth platform connections
 * 
 * Usage:
 * ```tsx
 * const { user, login, logout } = useAuthStore();
 * ```
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// ==================== Types ====================

interface User {
    id: number;
    username: string;
    email: string;
}

interface ConnectedAccount {
    platform: string;
    account_id: string;
    connected: boolean;
}

interface AuthState {
    // State
    user: User | null;
    token: string | null;
    connectedAccounts: ConnectedAccount[];
    isAuthenticated: boolean;

    // Actions
    login: (email: string, password: string) => Promise<void>;
    register: (username: string, email: string, password: string) => Promise<void>;
    logout: () => void;
    setToken: (token: string) => void;
    fetchConnectedAccounts: () => Promise<void>;
    connectPlatform: (platform: 'instagram' | 'twitter' | 'youtube') => void;
}

// ==================== Configuration ====================

// Backend API URL - change this for production
const API_URL = 'http://localhost:8000';

// ==================== Store ====================

export const useAuthStore = create<AuthState>()(
    persist(
        (set, get) => ({
            // Initial state
            user: null,
            token: null,
            connectedAccounts: [],
            isAuthenticated: false,

            /**
             * Login user with email and password
             * 
             * @param email - User's email
             * @param password - User's password
             * @throws Error if login fails
             */
            login: async (email: string, password: string) => {
                try {
                    const response = await fetch(`${API_URL}/auth/login`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password }),
                    });

                    if (!response.ok) {
                        throw new Error('Login failed');
                    }

                    const data = await response.json();

                    // Update state with user data and token
                    set({
                        token: data.access_token,
                        user: { id: data.user_id, email, username: email.split('@')[0] },
                        isAuthenticated: true,
                    });

                    // Fetch connected accounts after successful login
                    get().fetchConnectedAccounts();
                } catch (error) {
                    console.error('Login error:', error);
                    throw error;
                }
            },

            /**
             * Register a new user
             * 
             * @param username - Desired username
             * @param email - User's email
             * @param password - User's password
             * @throws Error if registration fails
             */
            register: async (username: string, email: string, password: string) => {
                try {
                    const response = await fetch(`${API_URL}/auth/register`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, email, password }),
                    });

                    if (!response.ok) {
                        throw new Error('Registration failed');
                    }

                    const data = await response.json();

                    // Update state with new user data
                    set({
                        token: data.access_token,
                        user: { id: data.user_id, email, username },
                        isAuthenticated: true,
                    });
                } catch (error) {
                    console.error('Registration error:', error);
                    throw error;
                }
            },

            /**
             * Logout user and clear all state
             */
            logout: () => {
                set({
                    user: null,
                    token: null,
                    connectedAccounts: [],
                    isAuthenticated: false,
                });
            },

            /**
             * Set JWT token manually
             * Used by OAuth callback handlers
             * 
             * @param token - JWT token string
             */
            setToken: (token: string) => {
                set({ token });
            },

            /**
             * Fetch list of connected social accounts
             * Called after login and OAuth connections
             */
            fetchConnectedAccounts: async () => {
                const { user, token } = get();
                if (!user || !token) return;

                try {
                    const response = await fetch(
                        `${API_URL}/social/connected-accounts?user_id=${user.id}`,
                        {
                            headers: { Authorization: `Bearer ${token}` },
                        }
                    );

                    if (response.ok) {
                        const data = await response.json();
                        set({ connectedAccounts: data.connected_accounts || [] });
                    }
                } catch (error) {
                    console.error('Error fetching connected accounts:', error);
                }
            },

            /**
             * Initiate OAuth connection for a platform
             * Redirects user to platform's OAuth page
             * 
             * @param platform - Platform to connect (instagram, twitter, youtube)
             */
            connectPlatform: (platform: 'instagram' | 'twitter' | 'youtube') => {
                // Redirect to backend OAuth endpoint
                // Backend will redirect to platform's OAuth page
                window.location.href = `${API_URL}/auth/${platform}`;
            },
        }),
        {
            // Persist configuration
            name: 'auth-storage', // LocalStorage key
            // Only persist these fields
            partialize: (state) => ({
                user: state.user,
                token: state.token,
                isAuthenticated: state.isAuthenticated,
            }),
        }
    )
);
