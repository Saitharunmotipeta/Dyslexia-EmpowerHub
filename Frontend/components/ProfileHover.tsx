"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { Icon } from "@/components/ui/Icon";
import { ICON_NAMES } from "@/constants/icons";
import { assetUrl } from "@/constants/assets";

export function ProfileHover() {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      return () => {
        document.removeEventListener("mousedown", handleClickOutside);
      };
    }
  }, [isOpen]);

  if (!user) return null;

  // Parse badges - expecting JSON string or comma-separated
  const parseBadges = (badgesStr: string | null): string[] => {
    if (!badgesStr) return [];
    try {
      const parsed = JSON.parse(badgesStr);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      // If not JSON, try comma-separated
      return badgesStr
        .split(",")
        .map((b) => b.trim())
        .filter((b) => b.length > 0);
    }
  };

  const badges = parseBadges(user.badges);
  const progress = Math.min(
    100,
    Math.round((user.points / Math.max(user.total_time_spent || 1, 1)) * 100)
  );

  return (
    <div
      ref={containerRef}
      className="relative"
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
    >
      {/* Profile Trigger Button */}
      <button
        type="button"
        className="rounded-xl px-3 py-2 text-sm font-medium text-dyslexia-text-secondary hover:bg-dyslexia-bg-secondary hover:text-dyslexia-text-primary transition-all duration-200 inline-flex items-center gap-1 leading-relaxed tracking-wide"
        aria-label="Profile menu"
        aria-expanded={isOpen}
      >
        <Icon name={ICON_NAMES.USER} size="sm" />
        <span className="hidden sm:inline">{user.name}</span>
      </button>

      {/* Profile Hover Card */}
      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-80 rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-primary shadow-lg z-50 overflow-hidden animate-in fade-in slide-in-from-top-2">
          {/* Header with Avatar and Basic Info */}
          <div className="bg-gradient-to-r from-[#6B8CA3]/10 to-[#4A6FA5]/10 px-6 py-5 border-b border-[#E8E4DC]">
            <div className="flex gap-3">
              {/* Avatar Placeholder */}
              <div className="h-12 w-12 rounded-full bg-gradient-to-br from-[#6B8CA3] to-[#4A6FA5] flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
                {user.name.charAt(0).toUpperCase()}
              </div>

              {/* Name and Email */}
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-dyslexia-text-primary truncate">
                  {user.name}
                </h3>
                <p className="text-xs text-dyslexia-text-secondary truncate">
                  {user.email}
                </p>
              </div>
            </div>
          </div>

          {/* Stats Section */}
          <div className="px-6 py-4 space-y-3 border-b border-[#E8E4DC]">
            {/* Levels Completed */}
            <div className="flex items-center justify-between">
              <span className="text-sm text-dyslexia-text-secondary">
                Levels Completed
              </span>
              <span className="font-semibold text-dyslexia-accent-blue">
                {user.courses_completed}
              </span>
            </div>

            {/* Progress Bar */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-sm text-dyslexia-text-secondary">
                  Progress
                </span>
                <span className="text-sm font-medium text-dyslexia-accent-blue">
                  {progress}%
                </span>
              </div>
              <div className="w-full h-2 bg-dyslexia-bg-secondary rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-[#6B8CA3] to-[#4A6FA5] rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>

            {/* Streak */}
            <div className="flex items-center justify-between pt-1">
              <span className="text-sm text-dyslexia-text-secondary">
                Streak
              </span>
              <span className="font-semibold text-dyslexia-text-primary">
                {user.streak_days} days 🔥
              </span>
            </div>
          </div>

          {/* Badges Section */}
          {badges.length > 0 && (
            <div className="px-6 py-4 border-b border-[#E8E4DC]">
              <h4 className="text-sm font-semibold text-dyslexia-text-primary mb-3">
                Badges
              </h4>
              <div className="flex flex-wrap gap-2">
                {badges.slice(0, 4).map((badge, idx) => (
                  <div
                    key={idx}
                    className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-[#FFD700]/10 text-sm text-dyslexia-text-primary"
                  >
                    <span>🏅</span>
                    <span className="font-medium">{badge}</span>
                  </div>
                ))}
                {badges.length > 4 && (
                  <div className="inline-flex items-center justify-center px-3 py-1.5 rounded-lg bg-dyslexia-bg-secondary text-xs font-medium text-dyslexia-text-secondary">
                    +{badges.length - 4} more
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="px-6 py-4 flex flex-col gap-2">
            <button
              type="button"
              onClick={() => logout()}
              className="w-full rounded-xl bg-red-500/10 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-500/20 transition-all duration-200 flex items-center justify-center gap-1 active:scale-95 transition-transform"
            >
              <Icon name={ICON_NAMES.LOGOUT} size="sm" />
              Logout
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
