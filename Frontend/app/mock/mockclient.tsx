"use client";

export const dynamic = "force-dynamic";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { learning, ApiError, type LevelOut } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { DifficultyBadge } from "@/components/ui/DifficultyBadge";

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
          href="/learning"
          className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900"
        >
          ← Back
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-gray-900">Mock test</h1>
        <p className="mt-1 text-gray-600">Choose a level to start a mock test.</p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {levels.filter((l) => l.is_unlocked).map((level) => (
          <Card key={level.id} padding="lg">
            <DifficultyBadge difficulty={level.difficulty || "medium"} />
            <h2 className="mt-3 text-xl font-bold text-gray-900">Level {level.order}</h2>
            <p className="mt-1 text-gray-600">{level.description || level.name}</p>
            <Button
              variant="primary"
              className="mt-4 w-full"
              onClick={() => startMock(level.id)}
            >
              Start mock test
            </Button>
          </Card>
        ))}
      </div>
    </div>
  );
}
