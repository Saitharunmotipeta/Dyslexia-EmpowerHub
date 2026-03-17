"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { dynamicApi, ApiError, type DynamicAnalyzeOut } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { PlaceholderMedia } from "@/components/ui/PlaceholderMedia";

const STEPS = 5;
const STEP_LABELS = ["Enter text", "Analyze", "See meaning", "Practice", "Done"];

export default function DynamicPage() {
  const router = useRouter();
  const { token, checked } = useAuth();
  const [step, setStep] = useState(1);
  const [text, setText] = useState("");
  const [analyzed, setAnalyzed] = useState<DynamicAnalyzeOut | null>(null);
  const [spoken, setSpoken] = useState("");
  const [score, setScore] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!checked) return;
    if (!token) router.push("/auth/login");
  }, [token, checked, router]);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await dynamicApi.analyze({ text: text.trim() });
      setAnalyzed(res);
      setStep(2);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Analyze failed");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveAttempt = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!analyzed) return;
    setLoading(true);
    setError(null);
    try {
      await dynamicApi.attempt({
        text: text.trim(),
        text_type: analyzed.type,
        spoken: spoken.trim() || " ",
        score: score ?? 0,
        pace: 1,
      });
      setStep(5);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Save failed");
    } finally {
      setLoading(false);
    }
  };

  if (!checked || !token) return null;

  const progressPct = (step / STEPS) * 100;

  return (
    <div className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-amber-100 text-amber-700 hover:bg-amber-200 transition-all duration-200 transform hover:scale-105 active:scale-95 font-medium text-sm shadow-soft"
        >
          <ArrowLeft size={18} className="transition-transform group-hover:-translate-x-1" />
          Back to Dashboard
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-gray-900">Dynamic learning</h1>
        <p className="mt-1 text-gray-600">Type or say the word you see.</p>
      </div>

      <Card className="space-y-6" padding="lg">
        <div className="flex items-center justify-between gap-4">
          <ProgressBar value={progressPct} className="flex-1" />
          <span className="text-sm font-medium text-gray-600">
            {step} / {STEPS}
          </span>
        </div>

        {step === 1 && (
          <>
            <PlaceholderMedia type="image" label="Word or sentence" />
            <form onSubmit={handleAnalyze} className="space-y-4">
              <Input
                label="Type or paste text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Type the word here..."
                required
              />
              <Button type="submit" loading={loading} className="w-full">
                Analyze
              </Button>
            </form>
          </>
        )}

        {step === 2 && analyzed && (
          <>
            <p className="text-xl font-semibold text-gray-900">
              Type: <span className="text-primary-600">{analyzed.type}</span>
            </p>
            <div className="rounded-2xl bg-gray-50 p-4">
              <p className="text-2xl font-bold uppercase tracking-wide text-gray-900">
                {analyzed.words.join(" ")}
              </p>
            </div>
            <p className="text-gray-600">
              <span className="font-medium">Meaning:</span> {analyzed.meaning}
            </p>
            <div className="flex gap-2">
              <Button variant="secondary" onClick={() => setStep(1)}>
                Back
              </Button>
              <Button onClick={() => setStep(3)}>Next: Practice</Button>
            </div>
          </>
        )}

        {step === 3 && analyzed && (
          <>
            <PlaceholderMedia type="audio" label="Listen" />
            <p className="text-center text-2xl font-bold uppercase text-gray-900">
              {analyzed.words.join(" ")}
            </p>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                setScore(80);
                setStep(4);
              }}
              className="space-y-4"
            >
              <Input
                label="Type or say the word"
                value={spoken}
                onChange={(e) => setSpoken(e.target.value)}
                placeholder="Type the word here..."
              />
              <Button type="submit" className="w-full">
                Submit & see score
              </Button>
            </form>
          </>
        )}

        {step === 4 && analyzed && (
          <form onSubmit={handleSaveAttempt} className="space-y-4">
            <p className="text-lg text-gray-700">
              Score: <strong>{score ?? 0}%</strong>. Save this attempt?
            </p>
            <Button type="submit" loading={loading} className="w-full">
              Save attempt
            </Button>
          </form>
        )}

        {step === 5 && (
          <>
            <p className="text-xl font-semibold text-green-600">Dynamic attempt saved.</p>
            <Button onClick={() => { setStep(1); setText(""); setAnalyzed(null); setSpoken(""); setScore(null); }}>
              Try again
            </Button>
            <Link href="/">
              <Button variant="outline">Home</Button>
            </Link>
          </>
        )}

        {error && (
          <p className="text-sm text-red-600" role="alert">
            {error}
          </p>
        )}
      </Card>
    </div>
  );
}
