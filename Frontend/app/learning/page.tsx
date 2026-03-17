"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowLeft, Book, Lock, CheckCircle2, Zap, Trophy } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { learning, ApiError, type LevelOut } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { DifficultyBadge } from "@/components/ui/DifficultyBadge";
import { Icon } from "@/components/ui/Icon";

export default function LearningPage() {
  const router = useRouter();
  const { token, checked } = useAuth();
  const [levels, setLevels] = useState<LevelOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!checked) return;
    if (!token) {
      router.push("/auth/login");
      return;
    }
    learning
      .getLevels()
      .then(setLevels)
      .catch((e) => setError(e instanceof ApiError ? e.message : "Failed to load levels"))
      .finally(() => setLoading(false));
  }, [token, checked, router]);

  if (!checked || !token) return null;
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white via-primary-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-pulse mb-4">
            <div className="w-12 h-12 bg-primary-400 rounded-full mx-auto"></div>
          </div>
          <p className="text-gray-600 text-lg font-medium">Loading your learning levels…</p>
        </div>
      </div>
    );
  }
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white via-primary-50 to-blue-50 flex items-center justify-center">
        <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 max-w-md">
          <p className="text-red-700 font-medium text-lg">{error}</p>
        </div>
      </div>
    );
  }

  const getDifficultyColor = (difficulty?: string) => {
    switch (difficulty?.toLowerCase()) {
      case "easy":
        return "from-green-400 to-emerald-500";
      case "medium":
        return "from-blue-400 to-indigo-500";
      case "hard":
        return "from-orange-400 to-red-500";
      default:
        return "from-primary-400 to-primary-500";
    }
  };

  const getDifficultyLightColor = (difficulty?: string) => {
    switch (difficulty?.toLowerCase()) {
      case "easy":
        return "bg-green-50";
      case "medium":
        return "bg-blue-50";
      case "hard":
        return "bg-red-50";
      default:
        return "bg-primary-50";
    }
  };

  const getDifficultyBorder = (difficulty?: string) => {
    switch (difficulty?.toLowerCase()) {
      case "easy":
        return "border-green-200";
      case "medium":
        return "border-blue-200";
      case "hard":
        return "border-red-200";
      default:
        return "border-primary-200";
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-white via-primary-50 to-blue-50">
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        {/* Header Section */}
        <div className="mb-12">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-100 text-primary-700 hover:bg-primary-200 transition-all duration-200 transform hover:scale-105 active:scale-95 font-medium text-sm shadow-soft"
          >
            <ArrowLeft size={18} />
            Back to Dashboard
          </Link>
          <div className="mt-6">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-2 leading-tight">
              Level-Based Learning
            </h1>
            <p className="text-xl text-gray-700 max-w-2xl leading-relaxed">
              Progress through carefully designed levels. Each level builds your skills step by step.
              Take your time and celebrate small wins!
            </p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid md:grid-cols-3 gap-4 mb-12">
          <div className="bg-white border-2 border-primary-200 rounded-2xl p-6 shadow-soft">
            <div className="flex items-center gap-3 mb-2">
              <Book size={24} className="text-primary-600" />
              <span className="text-sm font-medium text-gray-600">Total Levels</span>
            </div>
            <p className="text-3xl font-bold text-gray-900">{levels.length}</p>
          </div>
          <div className="bg-white border-2 border-blue-200 rounded-2xl p-6 shadow-soft">
            <div className="flex items-center gap-3 mb-2">
              <Zap size={24} className="text-blue-600" />
              <span className="text-sm font-medium text-gray-600">Started</span>
            </div>
            <p className="text-3xl font-bold text-gray-900">
              {levels.filter(l => l.is_unlocked).length}
            </p>
          </div>
          <div className="bg-white border-2 border-green-200 rounded-2xl p-6 shadow-soft">
            <div className="flex items-center gap-3 mb-2">
              <CheckCircle2 size={24} className="text-green-600" />
              <span className="text-sm font-medium text-gray-600">Completed</span>
            </div>
            <p className="text-3xl font-bold text-gray-900">
              {levels.filter(l => l.mastered_percentage === 100).length}
            </p>
          </div>
        </div>

        {/* Levels Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {levels.map((level, index) => (
            <div
              key={level.id}
              className={`transform transition-all duration-300 hover:scale-105 animate-fadeIn`}
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div
                className={`${getDifficultyLightColor(level.difficulty)} border-2 ${getDifficultyBorder(level.difficulty)} rounded-2xl p-6 shadow-soft hover:shadow-soft-lg flex flex-col h-full transition-all duration-300`}
              >
                {/* Level Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <div className={`bg-gradient-to-br ${getDifficultyColor(level.difficulty)} text-white rounded-lg px-3 py-1 text-sm font-bold`}>
                        Level {level.order}
                      </div>
                      <DifficultyBadge difficulty={level.difficulty || "medium"} />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900">
                      {level.name || `Level ${level.order}`}
                    </h2>
                  </div>
                </div>

                {/* Description */}
                <p className="text-gray-700 leading-relaxed text-base mb-4 flex-grow">
                  {level.description || `Master the skills in Level ${level.order}`}
                </p>

                {/* Progress Visualization */}
                <div className="mb-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-gray-700">Progress</span>
                    <span className="text-sm font-bold text-gray-900">
                      {Math.round(level.mastered_percentage ?? 0)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                    <div
                      className={`h-full bg-gradient-to-r ${getDifficultyColor(level.difficulty)} transition-all duration-500`}
                      style={{ width: `${level.mastered_percentage ?? 0}%` }}
                    ></div>
                  </div>
                </div>

                {/* Status Badge */}
                {level.mastered_percentage === 100 && (
                  <div className="mb-4 flex items-center gap-2 bg-green-100 border border-green-300 rounded-lg px-4 py-2">
                    <CheckCircle2 size={20} className="text-green-600" />
                    <span className="font-semibold text-green-700">Completed!</span>
                  </div>
                )}

                {/* Unlock Status */}
                {!level.is_unlocked && (
                  <div className="mb-4 flex items-center gap-2 bg-gray-100 border border-gray-300 rounded-lg px-4 py-2">
                    <Lock size={20} className="text-gray-600" />
                    <span className="font-semibold text-gray-700">Locked</span>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex flex-col gap-3">
                  {level.is_unlocked ? (
                    <>
                      <Link href={`/learning/${level.id}`} className="w-full">
                        <button className={`w-full bg-gradient-to-r ${getDifficultyColor(level.difficulty)} text-white font-bold py-3 px-4 rounded-xl transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-soft hover:shadow-soft-lg flex items-center justify-center gap-2`}>
                          <Book size={20} />
                          Continue Learning
                        </button>
                      </Link>
                      <Link href={`/mock/start?levelId=${level.id}`} className="w-full">
                        <button className="w-full bg-white border-2 border-gray-300 text-gray-900 font-bold py-3 px-4 rounded-xl transition-all duration-200 transform hover:scale-105 active:scale-95 hover:border-gray-400 hover:bg-gray-50 shadow-soft flex items-center justify-center gap-2">
                          <Trophy size={20} />
                          Take Test
                        </button>
                      </Link>
                    </>
                  ) : (
                    <div className="w-full bg-gray-100 text-gray-600 font-bold py-3 px-4 rounded-xl flex items-center justify-center gap-2 cursor-not-allowed opacity-60">
                      <Lock size={20} />
                      Locked
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Footer Message */}
        <div className="mt-16 text-center">
          <p className="text-gray-700 text-lg leading-relaxed">
            💚 Each level is designed with <span className="font-bold">dyslexia support</span> in mind.
            <br />
            Go at <span className="font-bold">your own pace</span> and celebrate every achievement!
          </p>
        </div>
      </div>

      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.6s ease-out forwards;
        }
      `}</style>
    </main>
  );
}
