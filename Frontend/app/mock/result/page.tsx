"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { mock, ApiError, type MockResultResponse } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";

export default function MockResultPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const attemptId = searchParams.get("public_attempt_id");

  const { token, checked } = useAuth();
  const [data, setData] = useState<MockResultResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!checked) return;
    if (!token) {
      router.push("/auth/login");
      return;
    }
    if (!attemptId) {
      setError("Missing attempt ID.");
      setLoading(false);
      return;
    }
    mock
      .getResult({ public_attempt_id: attemptId })
      .then(setData)
      .catch((e) => setError(e instanceof ApiError ? e.message : "Failed to load result"))
      .finally(() => setLoading(false));
  }, [attemptId, token, checked, router]);

  if (!checked || !token) return null;
  if (loading) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-gray-600">Loading result…</p>
      </div>
    );
  }
  if (error || !data) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-red-600">{error ?? "No result"}</p>
        <Link href="/mock" className="mt-4 inline-block text-primary-600 hover:underline">
          Back to mock test
        </Link>
      </div>
    );
  }

  const scorePct = Math.round(data.score);

  return (
    <div className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <h1 className="text-3xl font-bold text-gray-900">Mock test result</h1>
      <p className="mt-1 text-gray-600">{data.message}</p>

      <Card className="mt-8 space-y-6" padding="lg">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm text-gray-600">Score</p>
            <p className="text-3xl font-bold text-primary-600">{scorePct}%</p>
          </div>
          <ProgressBar value={scorePct} className="max-w-[200px]" />
        </div>
        <p className="text-lg font-semibold text-gray-900">Verdict: {data.verdict}</p>

        {data.words?.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Words</h2>
            <ul className="mt-2 space-y-2">
              {data.words.map((w: Record<string, unknown>, i: number) => (
                <li
                  key={i}
                  className="flex flex-wrap items-center gap-2 rounded-xl bg-gray-50 p-3"
                >
                  <span className="font-medium">{String(w.expected ?? "")}</span>
                  <span className="text-gray-500">→</span>
                  <span
                    className={
                      Number(w.score) >= 80 ? "text-green-600" : "text-red-600"
                    }
                  >
                    {String(w.spoken ?? "")} ({Number(w.score)}%)
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {data.tips?.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Tips</h2>
            <ul className="mt-2 list-inside list-disc text-gray-600">
              {data.tips.map((tip, i) => (
                <li key={i}>{tip}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="flex flex-wrap gap-4">
          <Link href={`/mock/report?public_attempt_id=${encodeURIComponent(data.public_attempt_id)}`}>
            <Button variant="primary">View report</Button>
          </Link>
          <Link href="/mock">
            <Button variant="outline">Another mock test</Button>
          </Link>
          <Link href="/learning">
            <Button variant="ghost">Back to learning</Button>
          </Link>
        </div>
      </Card>
    </div>
  );
}
