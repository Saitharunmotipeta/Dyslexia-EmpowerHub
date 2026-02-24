"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { mock, ApiError } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface ReportData {
  attempt_id: string;
  final_score: number;
  verdict: string;
  words: Array<Record<string, unknown>>;
  pdf_generated: boolean;
  message: string;
}

export default function MockReportPage() {
  const searchParams = useSearchParams();
  const attemptId = searchParams.get("public_attempt_id");

  const { token, checked } = useAuth();
  const [data, setData] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!checked) return;
    if (!token) return;
    if (!attemptId) {
      setError("Missing attempt ID.");
      setLoading(false);
      return;
    }
    mock
      .report(attemptId)
      .then(setData)
      .catch((e) => setError(e instanceof ApiError ? e.message : "Failed to load report"))
      .finally(() => setLoading(false));
  }, [attemptId, token, checked]);

  if (!checked || !token) return null;
  if (loading) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-gray-600">Loading report…</p>
      </div>
    );
  }
  if (error || !data) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-red-600">{error ?? "No report"}</p>
        <Link href="/mock" className="mt-4 inline-block text-primary-600 hover:underline">
          Back to mock test
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <h1 className="text-3xl font-bold text-gray-900">Mock test report</h1>
      <p className="mt-1 text-gray-600">{data.message}</p>

      <Card className="mt-8 space-y-6" padding="lg">
        <p className="text-lg">
          <span className="font-semibold text-gray-700">Score:</span>{" "}
          <span className="font-bold text-primary-600">{data.final_score}%</span>
        </p>
        <p className="text-lg">
          <span className="font-semibold text-gray-700">Verdict:</span>{" "}
          {data.verdict}
        </p>
        {data.pdf_generated && (
          <p className="text-sm text-gray-600">PDF generated on server.</p>
        )}

        {data.words?.length > 0 && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Word details</h2>
            <ul className="mt-2 space-y-2">
              {data.words.map((w: Record<string, unknown>, i: number) => (
                <li
                  key={i}
                  className="rounded-xl border border-gray-200 bg-gray-50 p-3"
                >
                  <p>
                    Expected: <strong>{String(w.expected ?? "")}</strong>
                  </p>
                  <p>
                    Spoken:{" "}
                    <span
                      className={
                        Number(w.score) >= 80 ? "text-green-600" : "text-red-600"
                      }
                    >
                      {String(w.spoken ?? "")}
                    </span>{" "}
                    ({Number(w.score)}%)
                  </p>
                  {w.feedback && (
                    <p className="mt-1 text-sm text-gray-600">
                      {String(w.feedback)}
                    </p>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="flex gap-4">
          <Link href="/mock">
            <Button variant="primary">New mock test</Button>
          </Link>
          <Link href="/learning">
            <Button variant="outline">Learning</Button>
          </Link>
        </div>
      </Card>
    </div>
  );
}
