"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { practice, learning, feedback, mapFeedbackResponse, ApiError, type WordStatusOut, type FeedbackResult } from "@/lib/api";
import { useDebounce } from "@/hooks/useDebounce";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { PlaceholderMedia } from "@/components/ui/PlaceholderMedia";
import { CompletionPopup } from "@/components/ui/CompletionPopup";
import { assetUrl } from "@/constants/assets";

const PACE_MIN = 1;
const PACE_MAX = 100;
const PACE_DEFAULT = 100;
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const dynamic = "force-dynamic";

export default function PracticePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const wordIdParam = searchParams.get("wordId");
  const levelIdParam = searchParams.get("levelId");
  const wordId = wordIdParam ? parseInt(wordIdParam, 10) : null;
  const levelId = levelIdParam ? parseInt(levelIdParam, 10) : null;

  const { token, checked } = useAuth();
  const [imgError, setImgError] = useState(false);
  const [currentWord, setCurrentWord] = useState<WordStatusOut | null>(null);
  const [pace, setPace] = useState(PACE_DEFAULT);
  const paceDebounced = useDebounce(pace, 300);
  const [recording, setRecording] = useState(false);
  const [result, setResult] = useState<FeedbackResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [wordLoading, setWordLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showWordCompletion, setShowWordCompletion] = useState(false);
  const [showRetry, setShowRetry] = useState(false);
  const [showNextGif, setShowNextGif] = useState(false);
  const wordCompletedThisSessionRef = useRef(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  // const [typedInput, setTypedInput] = useState("");

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    if (!checked) return;
    if (!token) {
      router.push("/auth/login");
      return;
    }
  }, [token, checked, router]);
  
  // Fetch word to show (expected word + visual hint) when we have wordId and levelId
  useEffect(() => {
    if (!token || !wordId || !levelId) {
      setCurrentWord(null);
      return;
    }
    setWordLoading(true);
    learning
      .getWordsForLevel(levelId)
      .then((words) => {
        const w = words.find((x) => x.id === wordId) ?? null;
        setCurrentWord(w);
      })
      .catch(() => setCurrentWord(null))
      .finally(() => setWordLoading(false));
  }, [token, wordId, levelId]);

  useEffect(() => {
    wordCompletedThisSessionRef.current = false;
  }, [wordId, levelId]);

  useEffect(() => {
    if (!showNextGif || !levelId || !wordId) return;
    const t = setTimeout(() => {
      learning
        .getWordsForLevel(levelId)
        .then((words) => {
          const idx = words.findIndex((w) => w.id === wordId);
          if (idx >= 0 && idx < words.length - 1) {
            const nextWord = words[idx + 1];
            router.push(`/practice?wordId=${nextWord.id}&levelId=${levelId}`);
          } else {
            router.push(`/learning/${levelId}`);
          }
        })
        .catch(() => router.push(`/learning/${levelId}`))
        .finally(() => setShowNextGif(false));
    }, 2000);
    return () => clearTimeout(t);
  }, [showNextGif, levelId, wordId, router]);

  const startRecording = useCallback(async () => {
    setError(null);
    setResult(null);
    setAudioBlob(null);
    setAudioURL(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;

      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        chunksRef.current.push(e.data);
      };

      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });

        setAudioBlob(blob);
        setAudioURL(URL.createObjectURL(blob));

        chunksRef.current = [];
      };

      recorder.start();
      setRecording(true);
    } catch {
      setError("Microphone access denied or unavailable.");
    }
  }, []);

  const stopRecording = useCallback(() => {
    const recorder = mediaRecorderRef.current;

    if (recorder && recorder.state === "recording") {
      recorder.stop();
      recorder.stream.getTracks().forEach((t) => t.stop());
    }

    // Clean recorder refs
    mediaRecorderRef.current = null;
    streamRef.current = null;
    setRecording(false);

  }, []);

  async function submitAudio() {
    if (!wordId) return;

    setLoading(true);
    setError(null);

    try {
      // -----------------------------
      // STEP 1: EVALUATE (audio → score)
      // -----------------------------
      const formData = new FormData();

      formData.append("word_id", String(wordId));
      formData.append(
        "file",
        audioBlob || new Blob([""], { type: "audio/webm" }),
        "audio.webm"
      );

      const evalRes = await fetch(`${API}/practice/evaluate`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!evalRes.ok) {
        throw new Error(await evalRes.text());
      }

      const evalData = await evalRes.json();

      // -----------------------------
      // STEP 2: AGGREGATE (intelligence layer)
      // -----------------------------
      const aggRes = await fetch(`${API}/feedback/aggregate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          mode: "static",
          content_type: "word",
          text: evalData.expected,
          spoken: evalData.recognized,
          score: evalData.score,
          attempts: 1,
          pace: 0.9,
        }),
      });

      if (!aggRes.ok) {
        throw new Error(await aggRes.text());
      }

      const aggData = await aggRes.json();

      // -----------------------------
      // STEP 3: MAP → UI MODEL (FeedbackResult)
      // -----------------------------
      const clean: FeedbackResult = {
        expected: evalData.expected,
        spoken: evalData.recognized,
        score: evalData.score,

        pattern: aggData.pattern?.pattern?.code,
        feedback: aggData.feedback?.feedback || [],
        recommendation: aggData.recommendation?.headline,
        nextSteps: aggData.recommendation?.next_steps || [],
      };

      setResult(clean);

      // -----------------------------
      // STEP 4: UI FLOW
      // -----------------------------
      if (evalData.score >= 60) {
        setShowWordCompletion(true);
        setShowNextGif(true);
      } else {
        setShowRetry(true);
      }

      // -----------------------------
      // STEP 5: CLEANUP
      // -----------------------------
      setAudioBlob(null);
      setAudioURL(null);

    } catch (err) {
      console.error(err);
      setError("Evaluation failed");
    } finally {
      setLoading(false);
    }
  }

  function getAlignment(expected: string, spoken: string) {
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
  }

  // Play the expected word using browser TTS at current pace (backend-style: pace 50–150 → rate 0.5–1.5)
  const playWord = useCallback(() => {
    const word = currentWord?.text ?? result?.expected;
    if (!word) return;
    if (typeof window === "undefined" || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(word);
    u.lang = "en-US";
    u.rate = paceDebounced / 100; 
    window.speechSynthesis.speak(u);
  }, [currentWord?.text, result?.expected, paceDebounced]);

  const displayWord =currentWord?.text ?? currentWord?.text ?? result?.expected ?? "";
  useEffect(() => {
    setImgError(false);
  }, [displayWord]);
  if (!checked || !token) return null;

  const wordKey = displayWord
  ?.toLowerCase()
  .trim()
  .replace(/\s+/g, "")
  .replace(/[^a-z]/g, ""); 
 
  const dynamicImage = wordKey ? assetUrl(`${wordKey}.jpg`) : null;

  const finalImage =
  currentWord?.image_url && currentWord.image_url.trim() !== "" && !imgError
    ? currentWord.image_url
    : dynamicImage;

  return (
    <div className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <Link
          href="/learning"
          className="inline-flex items-center text-sm font-medium text-dyslexia-text-secondary hover:text-dyslexia-text-primary transition-all duration-200 leading-relaxed tracking-wide"
        >
          ← Back
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-dyslexia-text-primary leading-relaxed tracking-wide">Voice test</h1>
        <p className="mt-1 text-dyslexia-text-secondary leading-relaxed tracking-wide">
          Record or type the word. We&apos;ll compare it to the expected word.
        </p>
      </div>

      <Card className="space-y-6" padding="lg">
        {!wordId || !levelId ? (
          <p className="text-dyslexia-accent-purple leading-relaxed tracking-wide">
            Open this page from Learning → choose a level → Practice on a word.
          </p>
        ) : wordLoading ? (
          <p className="text-dyslexia-text-secondary leading-relaxed tracking-wide">Loading word…</p>
        ) : (
          <>
            {/* Visual hint: image from backend if available, else placeholder */}
            <div className="h-[320px] w-full overflow-hidden rounded-xl bg-dyslexia-bg-secondary flex items-center justify-center">
              {finalImage ? (
                <img
                  src={finalImage}
                  alt={displayWord}
                  className="h-full w-full object-contain rounded-xl"
                  onError={() => setImgError(true)}
                />
              ) : (
                <PlaceholderMedia
                  type="image"
                  label={`Visual hint for ${displayWord || "word"}`}
                  className="min-h-[160px]"
                />
              )}
            </div>

            {/* Word to speak — large and readable */}
            <p className="text-center text-2xl font-bold uppercase tracking-wide text-dyslexia-text-primary sm:text-3xl leading-relaxed">
              {displayWord || "—"}
            </p>
            {currentWord?.phonetics && (
              <p className="text-center text-lg text-dyslexia-text-secondary leading-relaxed tracking-wide">{currentWord.phonetics}</p>
            )}
            {currentWord?.syllables && (
              <p className="text-center text-sm text-dyslexia-text-secondary">{currentWord.syllables}</p>
            )}

            {/* Play word (TTS) at current pace */}
            <div className="flex flex-wrap items-center gap-4">
              <Button
                variant="outline"
                onClick={playWord}
                disabled={!displayWord}
                type="button"
                aria-label="Play word"
              >
                <span className="mr-2" aria-hidden>🔊</span>
                Play word
              </Button>
              {/* Record Button */}
              <Button
                variant={recording ? "secondary" : "primary"}
                onClick={recording ? stopRecording : startRecording}
                disabled={!wordId}
                aria-pressed={recording}
              >
                {recording ? "Stop" : "Record"}
              </Button>
              </div>

              {/* Text Input (Unified) */}
              {/* <input
                type="text"
                placeholder="Type the word (optional)..."
                value={typedInput}
                onChange={(e) => setTypedInput(e.target.value)}
                className="w-full rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-secondary px-4 py-3 focus:border-dyslexia-accent-blue focus:outline-none focus:ring-2 focus:ring-dyslexia-accent-blue/20 transition-all duration-200 leading-relaxed tracking-wide"
              /> */}

              {/* Audio Preview */}
              {audioURL && (
                <div className="mt-4 space-y-3">
                  <audio controls src={audioURL} className="w-full" />

                  <div className="flex gap-3">
                    <Button
                      variant="secondary"
                      onClick={() => {
                        setResult(null);
                        setAudioBlob(null);
                        setAudioURL(null);
                        startRecording();
                      }}
                    >
                      Retry
                    </Button>
                  </div>
                </div>
              )}

              {/* Single Submit Button */}
              <Button
                onClick={submitAudio}
                disabled={loading || !wordId}
                className="w-full mt-3"
              >
                {loading ? "Processing..." : "Submit"}
              </Button>

              {/* Loading Indicator */}
              {loading && (
                <div className="flex items-center gap-2 text-sm text-dyslexia-text-secondary mt-2">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-gray-300 border-t-blue-500"></div>
                  Processing your response...
                </div>
              )}

              {/* Playback Pace */}
              <div>
                <label className="block text-sm font-medium text-dyslexia-text-primary">
                  Playback pace: {pace}%
                </label>

                <input
                  type="range"
                  min={PACE_MIN}
                  max={PACE_MAX}
                  value={pace}
                  onChange={(e) => setPace(Number(e.target.value))}
                  className="mt-2 w-full accent-[#6B8CA3]"
                />

                <p className="mt-1 text-sm text-dyslexia-text-secondary">
                  Debounced value: {paceDebounced}%
                </p>
              </div>
          </>
        )}

        {error && (
          <p className="text-sm text-dyslexia-accent-purple" role="alert">
            {error}
          </p>
        )}

        <CompletionPopup
          open={showWordCompletion}
          onClose={() => setShowWordCompletion(false)}
          imageSrc={assetUrl("levelcompletion.gif")}
          imageAlt="Word completion"
          variant="success"
        >
          Yay! You reached {result?.score ?? 0}% mastery
        </CompletionPopup>
        <CompletionPopup
          open={showRetry}
          onClose={() => setShowRetry(false)}
          imageSrc={assetUrl("retry.gif")}
          imageAlt="Try again"
          variant="retry"
        >
          Try again to improve your mastery
        </CompletionPopup>
          {result && (
            <div className="rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-secondary p-4 space-y-4">

              {/* Expected vs Spoken */}
              {/* 🔥 Expected vs Spoken */}
            <div>
              {(() => {
                const alignment = getAlignment(result.expected, result.spoken);

                return (
                  <>
                    {/* Expected */}
                    <p className="text-sm text-gray-500">Expected</p>
                    <div className="flex flex-wrap gap-2">
                      {alignment.map((item, i) => (
                        <span key={i} className="px-2 py-1 rounded bg-gray-100">
                          {item.expected || "-"}
                        </span>
                      ))}
                    </div>

                    {/* Spoken */}
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

                    <p className="text-xs text-gray-500 mt-2">
                      Green = correct, Red = wrong, Yellow = missing, Purple = extra
                    </p>
                  </>
                );
              })()}
            </div>

              {/* Score */}
              <p className={`font-semibold ${
                result.score > 80 ? "text-green-600" :
                result.score > 50 ? "text-yellow-600" :
                "text-red-600"
              }`}>
                Score: {result.score}%
              </p>

              {/* Pattern */}
              {result.pattern && (
                <p className="text-sm text-purple-600">
                  Pattern: {result.pattern.replace("_", " ")}
                </p>
              )}

              {/* Feedback */}
              <div>
                <p className="font-semibold text-sm mb-1">Feedback</p>
                <ul className="list-disc ml-5 space-y-1 text-sm">
                  {result.feedback.map((f, i) => (
                    <li key={i}>{f}</li>
                  ))}
                </ul>
              </div>

              {/* Recommendation */}
              {result.recommendation && (
                <div>
                  <p className="font-semibold text-sm">Recommendation</p>
                  <p className="text-sm text-purple-700">
                    {result.recommendation}
                  </p>
                </div>
              )}

              {/* Next Steps */}
              {result.nextSteps.length > 0 && (
                <div>
                  <p className="font-semibold text-sm mb-1">Practice Words</p>
                  <div className="flex flex-wrap gap-2">
                    {result.nextSteps.map((word, i) => (
                      <span
                        key={i}
                        className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                      >
                        {word}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
      </Card>
    </div>
  );
}
