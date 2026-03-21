"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { practice, learning, ApiError, type EvaluationResponse, type WordStatusOut } from "@/lib/api";
import { useDebounce } from "@/hooks/useDebounce";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { PlaceholderMedia } from "@/components/ui/PlaceholderMedia";
import { CompletionPopup } from "@/components/ui/CompletionPopup";
import { assetUrl } from "@/constants/assets";

const PACE_MIN = 20;
const PACE_MAX = 140;
const PACE_DEFAULT = 100;

export const dynamic = "force-dynamic";

export default function PracticePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const wordIdParam = searchParams.get("wordId");
  const levelIdParam = searchParams.get("levelId");
  const wordId = wordIdParam ? parseInt(wordIdParam, 10) : null;
  const levelId = levelIdParam ? parseInt(levelIdParam, 10) : null;

  const { token, checked } = useAuth();
  const [currentWord, setCurrentWord] = useState<WordStatusOut | null>(null);
  const [pace, setPace] = useState(PACE_DEFAULT);
  const paceDebounced = useDebounce(pace, 300);
  const [recording, setRecording] = useState(false);
  const [result, setResult] = useState<EvaluationResponse | null>(null);
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
  const [typedInput, setTypedInput] = useState("");

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

  const submitSpoken = useCallback(
    async (spoken: string) => {
      if (!wordId) {
        setError("Open this page from Learning (Practice on a word).");
        return;
      }
      setLoading(true);
      setError(null);
      setShowWordCompletion(false);
      setShowRetry(false);
      setShowNextGif(false);
      try {
        const res = await practice.evaluate({
          word_id: wordId,
          recognized_text: spoken || " ",
        });
        setResult(res);
        if (res.score >= 60) {
          setShowWordCompletion(true);
          setShowNextGif(true);
          wordCompletedThisSessionRef.current = true;
        } else {
          if (!wordCompletedThisSessionRef.current) {
            setShowRetry(true);
          }
        }
      } catch (err) {
        setError(err instanceof ApiError ? err.message : "Evaluation failed");
      } finally {
        setLoading(false);
      }
    },
    [wordId]
  );

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

/**
 * Handles form submission when user types in spoken text and submits.
 * Prevents default form submission, gets the spoken text from the input field,
 * trims it and calls submitSpoken with the trimmed text.
 */
    const handleTextSubmit = (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      const form = e.currentTarget;
      const input = form.querySelector<HTMLInputElement>('input[name="spoken"]');
      const text = input?.value?.trim() ?? "";
      submitSpoken(text);
    };

  async function submitAudio() {
    if (!wordId) return;

    setLoading(true);
    setError(null);

    try {
      let data;

      // ✅ PRIORITY: typed input
      if (typedInput.trim()) {
        const res = await practice.evaluate({
          word_id: wordId,
          recognized_text: typedInput,
        });

        data = res;

      } else if (audioBlob) {
        const formData = new FormData();
        formData.append("file", audioBlob);
        formData.append("word_id", String(wordId));

        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/practice/evaluate`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        });

        if (!res.ok) throw new Error();

        data = await res.json();

      } else {
        setError("Please record or type something.");
        setLoading(false);
        return;
      }

      setResult(data);

      if (data.score >= 60) {
        setShowWordCompletion(true);
        setShowNextGif(true);
      } else {
        setShowRetry(true);
      }

      // ✅ cleanup after submit
      setAudioBlob(null);
      setAudioURL(null);
      setTypedInput("");

    } catch {
      setError("Evaluation failed");
    } finally {
      setLoading(false);
    }
  }

  // Play the expected word using browser TTS at current pace (backend-style: pace 50–150 → rate 0.5–1.5)
  const playWord = useCallback(() => {
    const word = currentWord?.text ?? result?.expected;
    if (!word) return;
    if (typeof window === "undefined" || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(word);
    u.lang = "en-US";
    u.rate = paceDebounced / 100; // 50 → 0.5, 100 → 1, 150 → 1.5
    window.speechSynthesis.speak(u);
  }, [currentWord?.text, result?.expected, paceDebounced]);

  const displayWord = currentWord?.text ?? result?.expected ?? "";

  if (!checked || !token) return null;

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
            <div className="min-h-[160px] overflow-hidden rounded-xl bg-dyslexia-bg-secondary transition-all duration-300">
              {currentWord?.image_url ? (
                <img
                  src={currentWord.image_url}
                  alt={displayWord}
                  className="h-full w-full object-contain rounded-xl"
                />
              ) : (
                <PlaceholderMedia type="image" label={`Visual hint for ${displayWord || "word"}`} className="min-h-[160px]" />
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
              <input
                type="text"
                placeholder="Type the word (optional)..."
                value={typedInput}
                onChange={(e) => setTypedInput(e.target.value)}
                className="w-full rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-secondary px-4 py-3 focus:border-dyslexia-accent-blue focus:outline-none focus:ring-2 focus:ring-dyslexia-accent-blue/20 transition-all duration-200 leading-relaxed tracking-wide"
              />

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
          <div className="rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-secondary p-4 transition-all duration-300">
            <p className="text-sm font-medium text-dyslexia-text-primary leading-relaxed tracking-wide">Transcript</p>
            <p className="mt-1 text-lg leading-relaxed tracking-wide">
              Expected: <span className="font-semibold text-dyslexia-text-primary">{result.expected}</span>
            </p>
            <p className="mt-1 text-lg leading-relaxed tracking-wide">
              You said:{" "}
              <span
                className={
                  result.is_correct
                    ? "font-semibold text-dyslexia-accent-green"
                    : "font-semibold text-dyslexia-accent-blue"
                }
              >
                {result.recognized || "(empty)"}
              </span>
            </p>
            <p className="mt-2 text-sm text-dyslexia-text-secondary">
              Score: {result.score}% · {result.is_correct ? "Correct" : "Incorrect"}
            </p>
          </div>
        )}
      </Card>
    </div>
  );
}
