"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { feedback, ApiError, type FeedbackIn } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export default function FeedbackPage() {
  const router = useRouter();
  const { token, checked } = useAuth();
  const [mode, setMode] = useState<"static" | "dynamic">("static");
  const [contentType, setContentType] = useState<"word" | "phrase" | "sentence">("word");
  const [text, setText] = useState("");
  const [spoken, setSpoken] = useState("");
  const [score, setScore] = useState(80);
  const [attempts, setAttempts] = useState(1);
  const [pace, setPace] = useState(0.9);
  const [result, setResult] = useState<{
    trend?: unknown;
    pattern?: unknown;
    feedback?: unknown;
    recommendation?: { headline: string; explanation: string; next_steps: string[] };
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!checked) return;
    if (!token) router.push("/auth/login");
  }, [token, checked, router]);

  const payload: FeedbackIn = {
    mode,
    content_type: contentType,
    text,
    spoken,
    score,
    attempts,
    pace,
  };

  const handleAggregate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await feedback.aggregate(payload);
      setResult(res);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  };

  if (!checked || !token) return null;

  return (
    <div className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <Link
          href="/"
          className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900"
        >
          ← Back
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-gray-900">Feedback</h1>
        <p className="mt-1 text-gray-600">Get trend, pattern, and recommendations.</p>
      </div>

      <Card className="space-y-6" padding="lg">
        <form onSubmit={handleAggregate} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Mode</label>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value as "static" | "dynamic")}
              className="mt-1 w-full rounded-2xl border border-gray-300 bg-gray-50 px-4 py-3 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-200"
            >
              <option value="static">Static</option>
              <option value="dynamic">Dynamic</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Content type</label>
            <select
              value={contentType}
              onChange={(e) =>
                setContentType(e.target.value as "word" | "phrase" | "sentence")
              }
              className="mt-1 w-full rounded-2xl border border-gray-300 bg-gray-50 px-4 py-3 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-200"
            >
              <option value="word">Word</option>
              <option value="phrase">Phrase</option>
              <option value="sentence">Sentence</option>
            </select>
          </div>
          <Input
            label="Expected text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            required
          />
          <Input
            label="Spoken text"
            value={spoken}
            onChange={(e) => setSpoken(e.target.value)}
          />
          <Input
            label="Score (0–100)"
            type="number"
            min={0}
            max={100}
            value={score}
            onChange={(e) => setScore(Number(e.target.value))}
          />
          <Input
            label="Attempts"
            type="number"
            min={1}
            value={attempts}
            onChange={(e) => setAttempts(Number(e.target.value))}
          />
          <Input
            label="Pace (optional)"
            type="number"
            step={0.1}
            value={pace}
            onChange={(e) => setPace(Number(e.target.value))}
          />
          <Button type="submit" loading={loading} className="w-full">
            Get aggregate feedback
          </Button>
        </form>

        {error && (
          <p className="text-sm text-red-600" role="alert">
            {error}
          </p>
        )}

        {result && (
          <div className="mt-6 space-y-4 rounded-2xl border border-gray-200 bg-gray-50 p-4">
            <h2 className="text-lg font-semibold text-gray-900">Result</h2>
            {result.trend != null && (
              <p><strong>Trend:</strong> {JSON.stringify(result.trend)}</p>
            )}
            {result.pattern != null && (
              <p><strong>Pattern:</strong> {JSON.stringify(result.pattern)}</p>
            )}
            {result.feedback != null && (
              <p><strong>Feedback:</strong> {JSON.stringify(result.feedback)}</p>
            )}
            {result.recommendation && (
              <div>
                <p className="font-medium">{result.recommendation.headline}</p>
                <p className="text-gray-600">{result.recommendation.explanation}</p>
                {result.recommendation.next_steps?.length > 0 && (
                  <ul className="mt-2 list-inside list-disc text-sm text-gray-600">
                    {result.recommendation.next_steps.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        )}
      </Card>
    </div>
  );
}
