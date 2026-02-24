"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { mock, ApiError, type MockStartResponse } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { PlaceholderMedia } from "@/components/ui/PlaceholderMedia";

export default function MockRunPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const levelIdParam = searchParams.get("levelId");
  const levelId = levelIdParam ? parseInt(levelIdParam, 10) : null;

  const { token, checked } = useAuth();
  const [data, setData] = useState<MockStartResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [spoken, setSpoken] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!checked) return;
    if (!token) {
      router.push("/auth/login");
      return;
    }
    if (!levelId) {
      setError("Missing level. Go back and choose a level.");
      setLoading(false);
      return;
    }
    mock
      .start(levelId)
      .then(setData)
      .catch((e) => setError(e instanceof ApiError ? e.message : "Failed to start mock"))
      .finally(() => setLoading(false));
  }, [levelId, token, checked, router]);

  const currentWord = data?.words?.[currentIndex];
  const isLast = data && currentIndex >= data.words.length - 1;

  const handleSubmitWord = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!data || !currentWord) return;
    setSubmitting(true);
    try {
      await mock.submitWord({
        public_attempt_id: data.public_attempt_id,
        word_id: currentWord.id,
        spoken: spoken.trim() || " ",
      });
      setSpoken("");
      if (isLast) {
        router.push(`/mock/result?public_attempt_id=${encodeURIComponent(data.public_attempt_id)}`);
        return;
      }
      setCurrentIndex((i) => i + 1);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Submit failed");
    } finally {
      setSubmitting(false);
    }
  };

  if (!checked || !token) return null;
  if (loading) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-gray-600">Starting mock test…</p>
      </div>
    );
  }
  if (error && !data) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-red-600">{error}</p>
        <Button variant="outline" className="mt-4" onClick={() => router.push("/mock")}>
          Back to levels
        </Button>
      </div>
    );
  }
  if (!data) return null;

  return (
    <div className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <div className="mb-6 flex items-center justify-between">
        <span className="text-sm text-gray-600">
          Word {currentIndex + 1} of {data.words.length}
        </span>
      </div>

      <Card className="space-y-6" padding="lg">
        <PlaceholderMedia type="image" label="Word image" />
        <p className="text-center text-2xl font-bold text-gray-900">
          {currentWord?.word ?? "—"}
        </p>

        <form onSubmit={handleSubmitWord} className="space-y-4">
          <input
            type="text"
            value={spoken}
            onChange={(e) => setSpoken(e.target.value)}
            placeholder="Type or say the word..."
            className="w-full rounded-2xl border border-gray-300 bg-gray-50 px-4 py-3 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-200"
            autoFocus
          />
          <Button type="submit" disabled={submitting} className="w-full">
            {isLast ? "Finish test" : "Next word"}
          </Button>
        </form>

        {error && (
          <p className="text-sm text-red-600" role="alert">
            {error}
          </p>
        )}
      </Card>
    </div>
  );
}
