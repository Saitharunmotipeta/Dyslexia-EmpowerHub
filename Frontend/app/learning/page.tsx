"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { learning, ApiError, type LevelOut } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { DifficultyBadge } from "@/components/ui/DifficultyBadge";

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
      <div className="mx-auto max-w-4xl px-4 py-12">
        <p className="text-gray-600">Loading levels…</p>
      </div>
    );
  }
  if (error) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <Link
          href="/"
          className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900"
        >
          ← Back
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-gray-900">Level-based learning</h1>
        <p className="mt-1 text-gray-600">Choose your difficulty and start learning.</p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {levels.map((level) => (
          <Card key={level.id} className="flex flex-col" padding="lg">
            <div className="flex items-start justify-between gap-2">
              <DifficultyBadge difficulty={level.difficulty || "medium"} />
              <ProgressBar
                value={level.mastered_percentage ?? 0}
                variant="vertical"
                label={`${Math.round(level.mastered_percentage ?? 0)}%`}
              />
            </div>
            <h2 className="mt-3 text-xl font-bold text-gray-900">
              Level {level.order}
            </h2>
            <p className="mt-1 text-gray-600">{level.description || level.name}</p>
            <div className="mt-4 flex flex-wrap items-center gap-2">
              {level.is_unlocked ? (
                <>
                  <Link href={`/learning/${level.id}`}>
                    <Button variant="primary" className="w-full sm:w-auto">
                      Continue
                    </Button>
                  </Link>
                  <Link href={`/mock/start?levelId=${level.id}`}>
                    <Button variant="outline" className="w-full sm:w-auto">
                      Mock Test
                    </Button>
                  </Link>
                </>
              ) : (
                <span className="flex items-center gap-1.5 text-sm text-gray-500">
                  <span aria-hidden>🔒</span> Locked
                </span>
              )}
            </div>
            {level.mastered_percentage === 100 && (
              <p className="mt-2 flex items-center gap-1.5 text-sm text-success-600">
                <span aria-hidden>✓</span> Completed
              </p>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
}
