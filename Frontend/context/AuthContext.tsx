"use client";

import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  useMemo,
} from "react";
import { auth, ApiError, type ProfileResponse } from "@/lib/api";

const TOKEN_KEY = "access_token";

interface AuthState {
  token: string | null;
  user: ProfileResponse | null;
  loading: boolean;
  checked: boolean;
}

interface AuthContextValue extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>({
    token: null,
    user: null,
    loading: false,
    checked: false,
  });

  const persistToken = useCallback((token: string | null) => {
    if (typeof window === "undefined") return;
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    } else {
      localStorage.removeItem(TOKEN_KEY);
    }
  }, []);

  const loadStoredToken = useCallback(() => {
    if (typeof window === "undefined") return;
    const stored = localStorage.getItem(TOKEN_KEY);
    setState((s) => ({ ...s, token: stored, checked: true }));
  }, []);

  useEffect(() => {
    loadStoredToken();
  }, [loadStoredToken]);

  const refreshProfile = useCallback(async () => {
    const token = typeof window !== "undefined" ? localStorage.getItem(TOKEN_KEY) : null;
    if (!token) {
      setState((s) => ({ ...s, user: null, checked: true }));
      return;
    }
    try {
      const profile = await auth.profile();
      setState((s) => ({ ...s, user: profile, checked: true }));
    } catch {
      persistToken(null);
      setState((s) => ({ ...s, token: null, user: null, checked: true }));
    }
  }, [persistToken]);

  useEffect(() => {
    if (!state.checked || !state.token) return;
    if (state.token && !state.user && !state.loading) {
      refreshProfile();
    }
  }, [state.checked, state.token, state.user, state.loading, refreshProfile]);

  const login = useCallback(
    async (email: string, password: string) => {
      setState((s) => ({ ...s, loading: true }));
      try {
        const res = await auth.login(email, password);
        persistToken(res.access_token);
        setState((s) => ({
          ...s,
          token: res.access_token,
          user: null,
          loading: false,
        }));
        await refreshProfile();
      } catch (e) {
        setState((s) => ({ ...s, loading: false }));
        if (e instanceof ApiError) throw e;
        if (e instanceof Error) throw e;
        throw new Error("Login failed");
      }
    },
    [persistToken, refreshProfile]
  );

  const register = useCallback(
    async (username: string, email: string, password: string) => {
      setState((s) => ({ ...s, loading: true }));
      try {
        await auth.register({ username, email, password });
        setState((s) => ({ ...s, loading: false }));
      } catch (e) {
        setState((s) => ({ ...s, loading: false }));
        if (e instanceof ApiError) throw e;
        if (e instanceof Error) throw e;
        throw new Error("Registration failed");
      }
    },
    []
  );

  const logout = useCallback(() => {
    persistToken(null);
    setState({ token: null, user: null, loading: false, checked: true });
  }, [persistToken]);

  const value = useMemo<AuthContextValue>(
    () => ({
      ...state,
      login,
      register,
      logout,
      refreshProfile,
    }),
    [state, login, register, logout, refreshProfile]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
