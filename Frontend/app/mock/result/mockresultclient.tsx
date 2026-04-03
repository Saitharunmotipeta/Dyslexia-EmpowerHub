"use client";

export const dynamic = "force-dynamic";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { mock, ApiError, type MockResultResponse } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { CompletionPopup } from "@/components/ui/CompletionPopup";
import { assetUrl } from "@/constants/assets";

export default function MockResultPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const attemptId = searchParams.get("public_attempt_id");

  const { token, checked } = useAuth();
  const [data, setData] = useState<MockResultResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showMockCompletion, setShowMockCompletion] = useState(false);

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
      .then((d) => {
        setData(d);
        setShowMockCompletion(true);
      })
      .catch((e) => setError(e instanceof ApiError ? e.message : "Failed to load result"))
      .finally(() => setLoading(false));
  }, [attemptId, token, checked, router]);

  useEffect(() => {
    if (!checked || !attemptId || !token) return;
    const url = `${process.env.NEXT_PUBLIC_API_BASE_URL}/mock/report?public_attempt_id=${attemptId}`;
    fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (res.ok) {
          console.log("[mock/report] success");
        } else {
          console.error("[mock/report] failed", res.status, res.statusText);
        }
      })
      .catch((err) => {
        console.error("[mock/report] failed", err);
      });
  }, [attemptId, token, checked]);

  if (!checked || !token) return null;
  if (loading) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-dyslexia-text-secondary leading-relaxed tracking-wide">Loading result…</p>
      </div>
    );
  }
  if (error || !data) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-dyslexia-accent-purple leading-relaxed tracking-wide">{error ?? "No result"}</p>
        <Link href="/mock" className="mt-4 inline-block text-dyslexia-accent-blue hover:underline transition-colors duration-200">
          Back to mock test
        </Link>
      </div>
    );
  }

  const scorePct = Math.round(data.score);

  return (
    <div className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <CompletionPopup
        open={showMockCompletion}
        onClose={() => setShowMockCompletion(false)}
        imageSrc={assetUrl("mockcompletion.gif")}
        imageAlt="Mock test completion"
      >
        {scorePct}% mastery. Report sent to mail
      </CompletionPopup>
      <h1 className="text-3xl font-bold text-dyslexia-text-primary leading-relaxed tracking-wide">Mock test result</h1>
      <p className="mt-1 text-dyslexia-text-secondary leading-relaxed tracking-wide">{data.message}</p>

      <Card className="mt-8 space-y-6 transition-all duration-300 ease-out" padding="lg">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm text-dyslexia-text-secondary leading-relaxed tracking-wide">Score</p>
            <p className="text-3xl font-bold text-dyslexia-accent-blue">{scorePct}%</p>
          </div>
          <ProgressBar value={scorePct} className="max-w-[200px]" />
        </div>
        <p className="text-lg font-semibold text-dyslexia-text-primary leading-relaxed tracking-wide">Verdict: {data.verdict}</p>

        {data.words?.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-dyslexia-text-primary leading-relaxed tracking-wide">Words</h2>
            <ul className="mt-2 space-y-2">
              {data.words.map((w: Record<string, unknown>, i: number) => (
                <li
                  key={i}
                  className="flex flex-wrap items-center gap-2 rounded-xl bg-dyslexia-bg-secondary p-3 leading-relaxed tracking-wide"
                >
                  <span className="font-medium text-dyslexia-text-primary">{String(w.expected ?? "")}</span>
                  <span className="text-dyslexia-text-secondary">→</span>
                  <span
                    className={
                      Number(w.score) >= 80 ? "text-dyslexia-accent-green" : "text-dyslexia-accent-blue"
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
            <h2 className="text-lg font-semibold text-dyslexia-text-primary leading-relaxed tracking-wide">Tips</h2>
            <ul className="mt-2 list-inside list-disc text-dyslexia-text-secondary leading-relaxed tracking-wide">
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
