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
import { assetUrl } from "@/constants/assets";

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
  const [isListening, setIsListening] = useState(false);
  const [pace, setPace] = useState(100);
  const [imgError, setImgError] = useState(false);

  useEffect(() => {
    if (!checked) return;
    if (!token) router.push("/auth/login");
  }, [token, checked, router]);

  useEffect(() => {
    setImgError(false);
  }, [analyzed]);

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

  const startListening = () => {
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;
  
    if (!SpeechRecognition) {
      alert("Speech Recognition not supported");
      return;
    }
  
    const recognition = new SpeechRecognition();
  
    recognition.lang = "en-US";
    recognition.interimResults = false;
  
    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
  
    recognition.onresult = (e: any) => {
      const transcript = e.results[0][0].transcript;
      setSpoken(transcript);
    };
  
    recognition.start();
  };

  const normalize = (t: string) =>
    t.toLowerCase().replace(/[^a-z\s]/g, "").trim();
  
  const calculateScore = (expected: string, spoken: string) => {
    const e = normalize(expected).split(" ");
    const s = normalize(spoken).split(" ");
  
    let correct = 0;
  
    e.forEach((word) => {
      if (s.includes(word)) correct++;
    });
  
    return Math.round((correct / e.length) * 100);
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

      {/* ✅ ADD IMAGE HERE (GLOBAL) */}
      <div className="h-[320px] w-full overflow-hidden rounded-xl bg-dyslexia-bg-secondary flex items-center justify-center">
        {dynamicImage && !imgError ? (
          <img
          src={dynamicImage || assetUrl("fallback.jpg")}
          alt={displayWord}
          className="h-full w-full object-contain rounded-xl"
          onError={(e) => {
            const target = e.currentTarget as HTMLImageElement;
            target.src = assetUrl("fallback.jpg");
          }}
        />
        ) : (
          <PlaceholderMedia
            type="image"
            label={`Visual hint for ${displayWord || "word"}`}
            className="min-h-[160px]"
          />
        )}
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
            <form
              onSubmit={(e) => {
                e.preventDefault();
                const scoreVal = calculateScore(analyzed.words.join(" "), spoken);
                setScore(scoreVal);
                setStep(4);
              }}
              className="space-y-4"
            >
              <Input
                label="Type or say the word"
                value={spoken}
                onChange={(e) => setSpoken(e.target.value)}
              />

              <div className="flex gap-2">
                <Button type="button" onClick={startListening}>
                  🎤 {isListening ? "Listening..." : "Speak"}
                </Button>

                <Button type="submit" className="flex-1">
                  Submit
                </Button>
              </div>
            </form>
          </>
        )}

        {step === 4 && analyzed && (
          <form onSubmit={handleSaveAttempt} className="space-y-4">

          {/* 🔥 ALIGNMENT UI */}
          {analyzed && spoken && (
            <div>
              {(() => {
                const alignment = getAlignment(
                  analyzed.words.join(" "),
                  spoken
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
                  </>
                );
              })()}
            </div>
          )}
        
          {/* SCORE */}
          <p className="text-lg">
            Score: <strong>{score ?? 0}%</strong>
          </p>
        
          <Button type="submit" loading={loading} className="w-full">
            Save attempt
          </Button>
        </form>
        )}

        {step === 5 && (
          <>
            <p className="text-xl font-semibold text-dyslexia-accent-green leading-relaxed tracking-wide">Dynamic attempt saved.</p>
            <Button onClick={() => { setStep(1); setText(""); setAnalyzed(null); setSpoken(""); setScore(null); }}>
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
