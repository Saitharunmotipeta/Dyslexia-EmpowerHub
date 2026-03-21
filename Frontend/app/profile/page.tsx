"use client";

import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { Icon } from "@/components/ui/Icon";
import { ICON_NAMES } from "@/constants/icons";
import { useEffect } from "react";

export default function ProfilePage() {
  const { user, checked, token } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (checked && !token) {
      router.push("/auth/login");
    }
  }, [checked, token, router]);

  if (!checked || !user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-dyslexia-accent-blue mx-auto mb-4"></div>
          <p className="text-dyslexia-text-secondary">Loading profile...</p>
        </div>
      </div>
    );
  }

  // Parse badges
  const parseBadges = (badgesStr: string | null): string[] => {
    if (!badgesStr) return [];
    try {
      const parsed = JSON.parse(badgesStr);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
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

  // Convert total_time_spent (seconds) to hours and minutes
  const totalHours = Math.floor(user.total_time_spent / 3600);
  const totalMinutes = Math.floor((user.total_time_spent % 3600) / 60);

  // Generate personalized motivational message
  const getMotivationalMessage = () => {
    if (user.streak_days >= 30) {
      return {
        emoji: "🌟",
        title: "You're On Fire!",
        message: `Amazing! You've maintained a ${user.streak_days}-day streak. Your consistency is inspiring!`,
      };
    } else if (user.streak_days >= 7) {
      return {
        emoji: "🚀",
        title: "Great Progress!",
        message: `You've built a ${user.streak_days}-day streak! Keep this momentum going.`,
      };
    } else if (user.courses_completed >= 5) {
      return {
        emoji: "💪",
        title: "You're Doing Amazing!",
        message: `You've completed ${user.courses_completed} levels. Every step is progress!`,
      };
    } else if (user.points >= 1000) {
      return {
        emoji: "⭐",
        title: "You're Rocking It!",
        message: `You've earned ${user.points.toLocaleString()} points. Keep learning and growing!`,
      };
    } else if (user.total_login_days >= 5) {
      return {
        emoji: "🎯",
        title: "You're Building a Habit!",
        message: `You've been with us for ${user.total_login_days} days. Consistency is key to success!`,
      };
    } else {
      return {
        emoji: "🌱",
        title: "Welcome to Your Learning Journey!",
        message: "You've just started! Every expert was once a beginner. Keep going!",
      };
    }
  };

  const motivation = getMotivationalMessage();

  return (
    <div className="min-h-screen bg-gradient-to-b from-dyslexia-bg-primary to-dyslexia-bg-secondary">
      <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
        {/* Profile Header */}
        <div className="rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-primary shadow-soft overflow-hidden mb-8">
          <div className="bg-gradient-to-r from-[#6B8CA3]/10 to-[#4A6FA5]/10 px-6 sm:px-8 py-8 border-b border-[#E8E4DC]">
            <div className="flex items-start gap-6">
              {/* Avatar */}
              <div className="h-24 w-24 rounded-full bg-gradient-to-br from-[#6B8CA3] to-[#4A6FA5] flex items-center justify-center text-white font-bold text-4xl flex-shrink-0">
                {user.name.charAt(0).toUpperCase()}
              </div>

              {/* User Info */}
              <div className="flex-1 min-w-0 pt-2">
                <h1 className="text-3xl font-bold text-dyslexia-text-primary mb-1">
                  {user.name}
                </h1>
                <p className="text-base text-dyslexia-text-secondary mb-3">
                  {user.email}
                </p>
                <div className="flex flex-wrap gap-4">
                  <div className="flex items-center gap-2 text-sm text-dyslexia-text-secondary">
                    <Icon name={ICON_NAMES.USER} size="sm" />
                    <span>{user.role}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm font-semibold text-red-600">
                    <span className="text-lg">🔥</span>
                    <span>{user.streak_days} day streak</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Motivational Banner */}
          <div className="bg-gradient-to-r from-[#FFD700]/15 via-[#4A6FA5]/5 to-[#6B8CA3]/15 py-6 px-6 sm:px-8 border-b border-[#E8E4DC]">
            <div className="flex items-start gap-4">
              <div className="text-4xl flex-shrink-0">{motivation.emoji}</div>
              <div className="flex-1 min-w-0">
                <h2 className="text-xl font-bold text-dyslexia-text-primary mb-1">
                  {motivation.title}
                </h2>
                <p className="text-base text-dyslexia-text-secondary leading-relaxed">
                  {motivation.message}
                </p>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 p-6 sm:p-8 border-b border-[#E8E4DC]">
            {/* Levels Completed */}
            <div className="rounded-xl bg-dyslexia-bg-secondary p-4">
              <div className="text-sm text-dyslexia-text-secondary mb-2">
                Levels Completed
              </div>
              <div className="text-3xl font-bold text-dyslexia-accent-blue">
                {user.courses_completed}
              </div>
            </div>

            {/* Points */}
            <div className="rounded-xl bg-dyslexia-bg-secondary p-4">
              <div className="text-sm text-dyslexia-text-secondary mb-2">
                Total Points
              </div>
              <div className="text-3xl font-bold text-[#6B8CA3]">
                {user.points.toLocaleString()}
              </div>
            </div>

            {/* Total Login Days */}
            <div className="rounded-xl bg-dyslexia-bg-secondary p-4">
              <div className="text-sm text-dyslexia-text-secondary mb-2">
                Total Login Days
              </div>
              <div className="text-3xl font-bold text-[#4A6FA5]">
                {user.total_login_days}
              </div>
            </div>

            {/* Time Spent */}
            <div className="rounded-xl bg-dyslexia-bg-secondary p-4">
              <div className="text-sm text-dyslexia-text-secondary mb-2">
                Time Spent
              </div>
              <div className="text-3xl font-bold text-[#6B8CA3]">
                {totalHours}h {totalMinutes}m
              </div>
            </div>
          </div>

          {/* Progress Section */}
          <div className="px-6 sm:px-8 py-6 border-b border-[#E8E4DC]">
            <div className="mb-2 flex items-center justify-between">
              <h3 className="text-sm font-semibold text-dyslexia-text-primary">
                Overall Progress
              </h3>
              <span className="text-lg font-bold text-dyslexia-accent-blue">
                {progress}%
              </span>
            </div>
            <div className="w-full h-3 bg-dyslexia-bg-secondary rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-[#6B8CA3] to-[#4A6FA5] rounded-full transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Badges Section */}
          <div className="px-6 sm:px-8 py-6">
            <h3 className="text-lg font-semibold text-dyslexia-text-primary mb-4">
              Badges & Achievements
            </h3>
            {badges.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {badges.map((badge, idx) => (
                  <div
                    key={idx}
                    className="flex items-center gap-3 p-4 rounded-xl bg-[#FFD700]/10 border border-[#FFD700]/20"
                  >
                    <span className="text-2xl">🏅</span>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-semibold text-dyslexia-text-primary truncate">
                        {badge}
                      </h4>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-dyslexia-bg-secondary text-center text-dyslexia-text-secondary">
                <p>No badges earned yet. Keep learning to unlock achievements!</p>
              </div>
            )}
          </div>
        </div>

        {/* Additional Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
          {/* User Info Card */}
          <div className="rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-primary shadow-soft p-6">
            <h3 className="text-lg font-semibold text-dyslexia-text-primary mb-4">
              Account Information
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-dyslexia-text-secondary">
                  User ID
                </span>
                <span className="font-medium text-dyslexia-text-primary">
                  #{user.id}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-dyslexia-text-secondary">
                  Role
                </span>
                <span className="font-medium text-dyslexia-text-primary capitalize">
                  {user.role}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-dyslexia-text-secondary">
                  Member Since
                </span>
                <span className="font-medium text-dyslexia-text-primary">
                  {user.total_login_days > 0
                    ? `${Math.ceil(user.total_login_days / 30)} months`
                    : "Recently"}
                </span>
              </div>
            </div>
          </div>

          {/* Activity Stats Card */}
          <div className="rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-primary shadow-soft p-6">
            <h3 className="text-lg font-semibold text-dyslexia-text-primary mb-4">
              Activity Stats
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-dyslexia-text-secondary">
                  Streak Days
                </span>
                <span className="font-medium text-red-600 flex items-center gap-1">
                  {user.streak_days}
                  <span className="text-lg">🔥</span>
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-dyslexia-text-secondary">
                  Completion Rate
                </span>
                <span className="font-medium text-dyslexia-accent-blue">
                  {user.courses_completed > 0 ? (user.courses_completed * 25).toLocaleString() : "0"}%
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-dyslexia-text-secondary">
                  Avg. Daily Time
                </span>
                <span className="font-medium text-dyslexia-text-primary">
                  {Math.round(user.total_time_spent / Math.max(user.total_login_days, 1))} min
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Motivational Footer Section */}
      <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="rounded-2xl border border-[#E8E4DC] bg-gradient-to-br from-[#6B8CA3]/5 to-[#4A6FA5]/5 shadow-soft p-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold text-dyslexia-text-primary mb-4">
              🎓 Your Learning Story
            </h3>
            <p className="text-lg text-dyslexia-text-secondary mb-6 leading-relaxed max-w-2xl mx-auto">
              {user.streak_days > 0
                ? `You've shown incredible dedication with your ${user.streak_days}-day streak. That's ${Math.round((user.streak_days / 365) * 100)}% of a year of consistency! 🎉`
                : "Start your streak today and unlock your full potential! Every day is an opportunity to learn and grow."}
            </p>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
              <div className="p-4 rounded-xl bg-dyslexia-bg-primary border border-[#E8E4DC]">
                <div className="text-2xl mb-2">📚</div>
                <div className="text-sm text-dyslexia-text-secondary">
                  {user.courses_completed} Levels
                </div>
              </div>
              <div className="p-4 rounded-xl bg-dyslexia-bg-primary border border-[#E8E4DC]">
                <div className="text-2xl mb-2">⏱️</div>
                <div className="text-sm text-dyslexia-text-secondary">
                  {totalHours}h {totalMinutes}m
                </div>
              </div>
              <div className="p-4 rounded-xl bg-dyslexia-bg-primary border border-[#E8E4DC]">
                <div className="text-2xl mb-2">🏆</div>
                <div className="text-sm text-dyslexia-text-secondary">
                  {badges.length} Badges
                </div>
              </div>
              <div className="p-4 rounded-xl bg-dyslexia-bg-primary border border-[#E8E4DC]">
                <div className="text-2xl mb-2">⭐</div>
                <div className="text-sm text-dyslexia-text-secondary">
                  {user.points} Points
                </div>
              </div>
            </div>

            <div className="bg-dyslexia-bg-primary rounded-xl p-6 border border-[#E8E4DC]">
              <p className="text-base text-dyslexia-text-primary font-semibold mb-2">
                💡 Pro Tip
              </p>
              <p className="text-sm text-dyslexia-text-secondary">
                Keep practicing to unlock the next level and build your confidence.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
