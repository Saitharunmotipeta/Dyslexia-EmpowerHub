"use client";

export const dynamic = "force-dynamic";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, Lock, CheckCircle2, Trophy, Zap } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { learning, ApiError, type LevelOut } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { DifficultyBadge } from "@/components/ui/DifficultyBadge";
import { assetUrl } from "@/constants/assets";

export default function MockStartPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const levelParam = searchParams.get("level");
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

  const startMock = (levelId: number) => {
    router.push(`/mock/start?levelId=${levelId}`);
  };

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

  if (!checked || !token) return null;
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-white via-primary-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-pulse mb-4">
            <div className="w-12 h-12 bg-primary-400 rounded-full mx-auto"></div>
          </div>
          <p className="text-gray-600 text-lg font-medium">Loading mock tests…</p>
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

  const unlockedCount = levels.filter(l => l.is_unlocked).length;
  const getLevelImage = (name?: string) => {
    if (!name) return null;
  
    const key = name
      .toLowerCase()
      .trim()
      .replace(/\s+/g, "-");
  
    return assetUrl(`${key}.jpg`);
  };
  return (
    <main className="min-h-screen bg-gradient-to-br from-white via-primary-50 to-blue-50">
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        {/* Header Section */}
        <div className="mb-12">
          <Link
            href="/learning"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-orange-100 text-orange-700 hover:bg-orange-200 transition-all duration-200 transform hover:scale-105 active:scale-95 font-medium text-sm shadow-soft"
          >
            <ArrowLeft size={18} />
            Back to Learning
          </Link>
          <div className="mt-6">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-2 leading-tight">
              Mock Tests
            </h1>
            <p className="text-xl text-gray-700 max-w-2xl leading-relaxed">
              Test your knowledge with mock exams. Each test evaluates your progress and 
              helps you identify areas for improvement. Take your time!
            </p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid md:grid-cols-2 gap-4 mb-12">
          <div className="bg-white border-2 border-orange-200 rounded-2xl p-6 shadow-soft">
            <div className="flex items-center gap-3 mb-2">
              <Trophy size={24} className="text-orange-600" />
              <span className="text-sm font-medium text-gray-600">Available Tests</span>
            </div>
            <p className="text-3xl font-bold text-gray-900">{unlockedCount}</p>
          </div>
          <div className="bg-white border-2 border-gray-200 rounded-2xl p-6 shadow-soft">
            <div className="flex items-center gap-3 mb-2">
              <Zap size={24} className="text-gray-600" />
              <span className="text-sm font-medium text-gray-600">Total Levels</span>
            </div>
            <p className="text-3xl font-bold text-gray-900">{levels.length}</p>
          </div>
        </div>

        {/* Mock Tests Grid */}
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
                
                {/* Header */}
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
                  {level.description || `Test your skills for Level ${level.order}`}
                </p>

                {/* Status */}
                {level.is_unlocked ? (
                  <>
                    <div className="mb-4 flex items-center gap-2 bg-green-100 border border-green-300 rounded-lg px-4 py-2">
                      <CheckCircle2 size={20} className="text-green-600" />
                      <span className="font-semibold text-green-700">Unlocked</span>
                    </div>
                    <button
                      onClick={() => startMock(level.id)}
                      className={`w-full bg-gradient-to-r ${getDifficultyColor(level.difficulty)} text-white font-bold py-3 px-4 rounded-xl transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-soft hover:shadow-soft-lg flex items-center justify-center gap-2`}
                    >
                      <Trophy size={20} />
                      Start Mock Test
                    </button>
                  </>
                ) : (
                  <>
                    <div className="mb-4 flex items-center gap-2 bg-gray-100 border border-gray-300 rounded-lg px-4 py-2">
                      <Lock size={20} className="text-gray-600" />
                      <span className="font-semibold text-gray-700">Locked</span>
                    </div>
                    <div className="w-full bg-gray-100 text-gray-600 font-bold py-3 px-4 rounded-xl flex items-center justify-center gap-2 cursor-not-allowed opacity-60">
                      <Lock size={20} />
                      Complete Previous Level
                    </div>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Footer Message */}
        <div className="mt-16 text-center">
          <p className="text-gray-700 text-lg leading-relaxed">
            💪 Mock tests are designed to help you learn, not just test.
            <br />
            Use them to <span className="font-bold">practice and improve</span> at your own pace!
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
