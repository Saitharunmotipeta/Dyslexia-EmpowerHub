"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { type DynamicAnalyzeOut } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { PlaceholderMedia } from "@/components/ui/PlaceholderMedia";
import { assetUrl } from "@/constants/assets";
import { useMediaRecorder } from "@/hooks/useMediaRecorder";
import { getPublicApiBaseUrl } from "@/lib/apiBase";
import {
  evaluateDynamicAudio,
  type PracticeEvaluation,
} from "@/lib/speech/evaluatePracticeAudio";

const STEPS = 5;
const STEP_LABELS = ["Enter text", "Analyze", "See meaning", "Practice", "Done"];
const API = getPublicApiBaseUrl();

export default function DynamicPage() {
  const router = useRouter();
  const { token, checked } = useAuth();
  const [step, setStep] = useState(1);
  const [text, setText] = useState("");
  const [analyzed, setAnalyzed] = useState<DynamicAnalyzeOut | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [evaluation, setEvaluation] = useState<PracticeEvaluation | null>(null);
  const [pace, setPace] = useState(100);
  const [imgError, setImgError] = useState(false);
  const [feedback, setFeedback] = useState<any>(null);
  const [attempts, setAttempts] = useState(1);

  const {
    recording,
    audioBlob,
    audioURL,
    error: micError,
    startRecording,
    stopRecording,
    reset,
  } = useMediaRecorder();

  useEffect(() => {
    if (!checked) return;
    if (!token) router.push("/auth/login");
  }, [token, checked, router]);

  useEffect(() => {
    setImgError(false);
  }, [analyzed]);

  useEffect(() => {
    if (!micError) return;
    setError(micError);
  }, [micError]);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    if (!token) {
      setError("Not authenticated.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/dynamic/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ text: text.trim() }),
      });

      if (!res.ok) throw new Error(await res.text());

      setAnalyzed((await res.json()) as DynamicAnalyzeOut);
      setEvaluation(null);
      reset();
      setStep(2);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analyze failed");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveAttempt = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!analyzed || !evaluation) return;
    if (!token) {
      setError("Not authenticated.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API}/dynamic/attempt`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          text: analyzed.words.join(" "),
          text_type: analyzed.type,
          spoken: evaluation.recognized.trim() || " ",
          score: evaluation.score ?? 0,
          pace: pace,
        }),
      });

      if (!res.ok) throw new Error(await res.text());

      const data = await res.json();

      console.log("Attempt ID:", data.attempt_id); // 🔥 you wanted this

      setStep(5);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Save failed");
    } finally {
      setLoading(false);
    }
  };

  if (!checked || !token) return null;

  const progressPct = (step / STEPS) * 100;

  const speak = (text: string, rate = pace / 100) => {
    if (!text || typeof window === "undefined") return;
  
    window.speechSynthesis.cancel();
  
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "en-US";
    u.rate = rate;
  
    window.speechSynthesis.speak(u);
  };
  
  const playText = () => {
    let t = text.trim();
    if (!t) return;
    if (!/[.!?]$/.test(t)) t += ".";
    speak(t);
  };
  
  const playMeaning = () => {
      if (!analyzed?.meaning) return;
      speak(analyzed.meaning, 0.9);
    };

  const handleEvaluateAudio = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!analyzed || !token) return;
    if (!audioBlob) {
      setError("Please record audio first.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const expected_text = analyzed.words.join(" ");

      // -------------------------------
      // 1. SPEECH SERVICE
      // -------------------------------
      const formData = new FormData();
      formData.append("file", audioBlob);

      const speechRes = await fetch(
        process.env.NEXT_PUBLIC_SPEECH_SERVICE_URL!,
        {
          method: "POST",
          body: formData,
        }
      );

      const speechData = await speechRes.json();

      const recognized_text =
        speechData.recognized_text ||
        speechData.text ||
        speechData.transcript ||
        "";

      if (!recognized_text) {
        throw new Error("No speech recognized");
      }

      // -------------------------------
      // 2. DYNAMIC EVALUATE
      // -------------------------------
      const evalRes = await fetch(`${API}/dynamic/evaluate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          expected_text,
          recognized_text,
        }),
      });

      if (!evalRes.ok) {
        throw new Error(await evalRes.text());
      }

      const evalData = await evalRes.json();

      setEvaluation(evalData);

      const getContentType = (text: string) => {
        const wordCount = text.trim().split(/\s+/).length;

        if (wordCount === 1) return "word";
        if (wordCount <= 5) return "phrase";
        return "sentence";
      };

      const type = analyzed.type;
      const newAttempts = attempts + 1;
      setAttempts(newAttempts);


      // -------------------------------
      // 3. FEEDBACK AGGREGATE
      // -------------------------------
      const feedbackRes = await fetch(`${API}/feedback/aggregate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          mode: "dynamic",                     
          content_type: type,                 
          text: evalData.expected,            
          spoken: evalData.recognized,        
          score: evalData.score,              
          attempts: newAttempts,                 
        }),
      });

      const feedbackData = await feedbackRes.json();
      setFeedback(feedbackData);

      reset();
      setStep(4);

    } catch (err) {
      setError(err instanceof Error ? err.message : "Evaluation failed");
    } finally {
      setLoading(false);
    }
  };

  const getAlignment = (expected: string, spoken: string) => {
    const exp = expected.toLowerCase().split(" ");
    const spk = spoken.toLowerCase().split(" ");
    const maxLen = Math.max(exp.length, spk.length);
  
    const alignment = [];
  
    for (let i = 0; i < maxLen; i++) {
      if (exp[i] === spk[i]) {
        alignment.push({ type: "correct", expected: exp[i], spoken: spk[i] });
      } else if (!spk[i]) {
        alignment.push({ type: "missing", expected: exp[i] });
      } else if (!exp[i]) {
        alignment.push({ type: "extra", spoken: spk[i] });
      } else {
        alignment.push({
          type: "substitution",
          expected: exp[i],
          spoken: spk[i],
        });
      }
    }
  
    return alignment;
  };

  const displayWord = analyzed?.words?.join(" ") || text;

  const wordKey = displayWord
    ?.toLowerCase()
    .trim()
    .replace(/\s+/g, "")
    .replace(/[^a-z]/g, "");

  const dynamicImage = wordKey ? assetUrl(`${wordKey}.jpg`) : null;

  const finalImage = dynamicImage;

  return (
    <div className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#6B8CA3]/15 text-dyslexia-accent-blue hover:bg-[#6B8CA3]/25 transition-all duration-200 hover:scale-105 active:scale-95 font-medium text-sm shadow-soft leading-relaxed tracking-wide"
        >
          <ArrowLeft size={18} className="transition-transform group-hover:-translate-x-1" />
          Back to Dashboard
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-dyslexia-text-primary leading-relaxed tracking-wide">Dynamic learning</h1>
        <p className="mt-1 text-dyslexia-text-secondary leading-relaxed tracking-wide">Type or say the word you see.</p>
      </div>

      <Card className="space-y-6" padding="lg">
        <div className="flex items-center justify-between gap-4">
          <ProgressBar value={progressPct} className="flex-1" />
          <span className="text-sm font-medium text-dyslexia-text-secondary leading-relaxed tracking-wide">
            {step} / {STEPS}
          </span>
        </div>

        <div className="flex justify-center">
          <img
            src={assetUrl("walk.gif")}
            alt=""
            className="h-20 w-auto object-contain sm:h-24 rounded-xl transition-opacity duration-300"
          />
        </div>

        <div>
        <label className="text-sm">Speed: {pace}%</label>
        <input
          type="range"
          min="1"
          max="100"
          value={pace}
          onChange={(e) => setPace(Number(e.target.value))}
          className="w-full"
        />
      </div>

        {step === 1 && (
          <>
            <form onSubmit={handleAnalyze} className="space-y-4">
              <Input
                label="Type or paste text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Type the word here..."
                required
              />
              <div className="flex gap-2">
                <Button type="submit" loading={loading} className="flex-1">
                  Analyze
                </Button>

                <Button type="button" onClick={playText}>
                  🔊
                </Button>
              </div>
            </form>
          </>
        )}

        {step === 2 && analyzed && (
          <>
            <p className="text-xl font-semibold text-dyslexia-text-primary leading-relaxed tracking-wide">
              Type: <span className="text-dyslexia-accent-blue">{analyzed.type}</span>
            </p>
            <div className="rounded-2xl bg-dyslexia-bg-secondary p-4 transition-all duration-300">
              <p className="text-2xl font-bold uppercase tracking-wide text-dyslexia-text-primary leading-relaxed">
                {analyzed.words.join(" ")}
              </p>
            </div>
            <p className="text-dyslexia-text-secondary leading-relaxed tracking-wide">
              <span className="font-medium">Meaning:</span> {analyzed.meaning}
            </p>
            <div className="flex gap-2">
              <Button onClick={() => speak(analyzed.words.join(" "))}>
                🔊 Play Word
              </Button>

              <Button onClick={playMeaning} variant="secondary">
                🔊 Play Meaning
              </Button>
            </div>
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
            <Button onClick={() => speak(analyzed.words.join(" "))}>
                🔊 Listen
              </Button>
            <p className="text-center text-2xl font-bold uppercase text-dyslexia-text-primary leading-relaxed tracking-wide">
              {analyzed.words.join(" ")}
            </p>
            <form onSubmit={handleEvaluateAudio} className="space-y-4">
              {audioURL && (
                <div className="mt-2 space-y-3">
                  <audio controls src={audioURL} className="w-full" />
                  <div className="flex gap-3">
                    <Button type="button" variant="secondary" onClick={reset}>
                      Retry
                    </Button>
                  </div>
                </div>
              )}

              <div className="flex gap-2">
                <Button
                  type="button"
                  onClick={recording ? stopRecording : startRecording}
                  disabled={!analyzed}
                  aria-pressed={recording}
                >
                  {recording ? "Stop" : "🎙 Record"}
                </Button>

                <Button type="submit" className="flex-1" disabled={loading || !audioBlob}>
                  {loading ? "Processing..." : "Submit"}
                </Button>
              </div>
            </form>
          </>
        )}

        {step === 4 && analyzed && (
          <form onSubmit={handleSaveAttempt} className="space-y-4">

          {/* 🔥 ALIGNMENT UI */}
          {evaluation && (
            <div>
              {(() => {
                const alignment = getAlignment(
                  evaluation.expected,
                  evaluation.recognized
                );
        
                return (
                  <>
                    <p className="text-sm text-gray-500">Expected</p>
                    <div className="flex flex-wrap gap-2">
                      {alignment.map((item, i) => (
                        <span key={i} className="px-2 py-1 rounded bg-gray-100">
                          {item.expected || "-"}
                        </span>
                      ))}
                    </div>
        
                    <p className="text-sm text-gray-500 mt-2">You said</p>
                    <div className="flex flex-wrap gap-2">
                      {alignment.map((item, i) => {
                        let color = "bg-gray-100";
        
                        if (item.type === "correct") color = "bg-green-200";
                        if (item.type === "substitution") color = "bg-red-200";
                        if (item.type === "missing") color = "bg-yellow-200";
                        if (item.type === "extra") color = "bg-purple-200";
        
                        return (
                          <span key={i} className={`px-2 py-1 rounded ${color}`}>
                            {item.spoken || "-"}
                          </span>
                        );
                      })}
                    </div>

                    <p className="text-xs text-gray-500 mt-3">
                      Verdict: <span className="font-medium">{evaluation.verdict || (evaluation.is_correct ? "correct" : "needs_practice")}</span>
                    </p>
                  </>
                );
              })()}
            </div>
          )}
        
          {/* SCORE */}
          <p className="text-lg">
            Score: <strong>{evaluation?.score ?? 0}%</strong>
          </p>
        
          <Button type="submit" loading={loading} className="w-full" disabled={!evaluation}>
            Save attempt
          </Button>
        </form>
        )}

        {step === 5 && (
          <>
            <p className="text-xl font-semibold text-dyslexia-accent-green leading-relaxed tracking-wide">Dynamic attempt saved.</p>
            <Button
              onClick={() => {
                setStep(1);
                setText("");
                setAnalyzed(null);
                setEvaluation(null);
                reset();
              }}
            >
              Try again
            </Button>
            <Link href="/">
              <Button variant="outline">Home</Button>
            </Link>
          </>
        )}

        {error && (
          <p className="text-sm text-dyslexia-accent-purple" role="alert">
            {error}
          </p>
        )}
      </Card>
    </div>
  );
}
