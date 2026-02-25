"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { learning, ApiError, type WordStatusOut } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function LevelWordsPage() {
  const router = useRouter();
  const params = useParams();
  const levelId = Number(params.levelId);
  const { token, checked } = useAuth();
  const [words, setWords] = useState<WordStatusOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!checked || !levelId) return;
    if (!token) {
      router.push("/auth/login");
      return;
    }
    learning
      .getWordsForLevel(levelId)
      .then(setWords)
      .catch((e) => {
        if (e instanceof ApiError && e.status === 403) {
          setError("Complete the previous level to unlock this one.");
        } else {
          setError(e instanceof ApiError ? e.message : "Failed to load words");
        }
      })
      .finally(() => setLoading(false));
  }, [levelId, token, checked, router]);

  if (!checked || !token) return null;
  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12">
        <p className="text-gray-600">Loading words…</p>
      </div>
    );
  }
  if (error) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12">
        <p className="text-red-600">{error}</p>
        <Link href="/learning" className="mt-4 inline-block text-primary-600 hover:underline">
          Back to levels
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <Link
          href="/learning"
          className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900"
        >
          ← Back to levels
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-gray-900">Level {levelId} words</h1>
        <p className="mt-1 text-gray-600">Practice these words.</p>
      </div>

      <div className="space-y-4">
        {words.map((w) => (
          <Card key={w.id} padding="md">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-lg font-semibold text-gray-900">{w.text}</p>
                {w.phonetics && (
                  <p className="text-sm text-gray-500">{w.phonetics}</p>
                )}
                <p className="mt-1 text-sm text-gray-600">
                  Mastery: {Math.round(w.mastery_score * 100)}% · Attempts: {w.attempts}
                  {w.is_mastered && (
                    <span className="ml-2 text-success-600">✓ Mastered</span>
                  )}
                </p>
              </div>
              <Link href={`/practice?wordId=${w.id}&levelId=${levelId}`}>
                <Button variant="secondary">Practice</Button>
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
