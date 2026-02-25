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

const PACE_MIN = 50;
const PACE_MAX = 150;
const PACE_DEFAULT = 100;

declare global {
  interface Window {
    SpeechRecognition?: new () => SpeechRecognition;
    webkitSpeechRecognition?: new () => SpeechRecognition;
  }
}
interface SpeechRecognitionEvent extends Event {
  readonly results: SpeechRecognitionResultList;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;

  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onerror: ((event: Event) => void) | null;
  onend: (() => void) | null;

  start(): void;
  stop(): void;
}
function getSpeechRecognition(): (new () => SpeechRecognition) | null {
  if (typeof window === "undefined") return null;
  return window.SpeechRecognition ?? window.webkitSpeechRecognition ?? null;
}

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

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const transcriptRef = useRef<string>("");
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const stopRequestedRef = useRef(false);

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

  const submitSpoken = useCallback(
    async (spoken: string) => {
      if (!wordId) {
        setError("Open this page from Learning (Practice on a word).");
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await practice.evaluate({
          word_id: wordId,
          recognized_text: spoken || " ",
        });
        setResult(res);
      } catch (err) {
        setError(err instanceof ApiError ? err.message : "Evaluation failed");
      } finally {
        setLoading(false);
      }
    },
    [wordId]
  );

  const submitSpokenRef = useRef(submitSpoken);
  submitSpokenRef.current = submitSpoken;

  const startRecording = useCallback(async () => {
    setError(null);
    setResult(null);
    transcriptRef.current = "";

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      const recorder = new MediaRecorder(stream);
      recorder.start();
      mediaRecorderRef.current = recorder;
      setRecording(true);

      const SR = getSpeechRecognition();
      if (SR) {
        stopRequestedRef.current = false;
        const recognition = new SR();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";
        recognition.onresult = (event: SpeechRecognitionEvent) => {
          transcriptRef.current = Array.from(event.results)
            .map((r) => r[0].transcript)
            .join(" ")
            .trim();
        };
        recognition.onerror = () => {};
        recognition.onend = () => {
          if (!stopRequestedRef.current) return;
          stopRequestedRef.current = false;
          const spoken = transcriptRef.current.trim();
          if (spoken) {
            submitSpokenRef.current(spoken);
          } else {
            setError("No speech detected. Type your answer below or try again.");
          }
        };
        recognition.start();
        recognitionRef.current = recognition;
      } else {
        setError("Speech recognition not supported in this browser. Use the text field.");
      }
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
    mediaRecorderRef.current = null;
    streamRef.current = null;

    const rec = recognitionRef.current;
    if (rec) {
      stopRequestedRef.current = true;
      try {
        rec.stop();
      } catch {
        // ignore
      }
      recognitionRef.current = null;
      // Transcript will be read in recognition.onend after the browser delivers final results
    } else {
      setRecording(false);
      const spoken = transcriptRef.current.trim();
      if (spoken) {
        submitSpoken(spoken);
      } else {
        setError("No speech detected. Type your answer below or try again.");
      }
    }

    setRecording(false);
  }, [submitSpoken]);

  const handleTextSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const input = form.querySelector<HTMLInputElement>('input[name="spoken"]');
    const text = input?.value?.trim() ?? "";
    submitSpoken(text);
  };

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
          className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900"
        >
          ← Back
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-gray-900">Voice test</h1>
        <p className="mt-1 text-gray-600">
          Record or type the word. We&apos;ll compare it to the expected word.
        </p>
      </div>

      <Card className="space-y-6" padding="lg">
        {!wordId || !levelId ? (
          <p className="text-amber-700">
            Open this page from Learning → choose a level → Practice on a word.
          </p>
        ) : wordLoading ? (
          <p className="text-gray-600">Loading word…</p>
        ) : (
          <>
            {/* Visual hint: image from backend if available, else placeholder */}
            <div className="min-h-[160px] overflow-hidden rounded-2xl bg-gray-100">
              {currentWord?.image_url ? (
                <img
                  src={currentWord.image_url}
                  alt={displayWord}
                  className="h-full w-full object-contain"
                />
              ) : (
                <PlaceholderMedia type="image" label={`Visual hint for ${displayWord || "word"}`} className="min-h-[160px]" />
              )}
            </div>

            {/* Word to speak — large and readable */}
            <p className="text-center text-2xl font-bold uppercase tracking-wide text-gray-900 sm:text-3xl">
              {displayWord || "—"}
            </p>
            {currentWord?.phonetics && (
              <p className="text-center text-lg text-gray-600">{currentWord.phonetics}</p>
            )}
            {currentWord?.syllables && (
              <p className="text-center text-sm text-gray-500">{currentWord.syllables}</p>
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
              <Button
                variant={recording ? "secondary" : "primary"}
                onClick={recording ? stopRecording : startRecording}
                disabled={!wordId}
                aria-pressed={recording}
              >
                {recording ? "Stop & submit" : "Record"}
              </Button>
            </div>

            <div>
              <label htmlFor="pace-slider" className="block text-sm font-medium text-gray-700">
                Playback pace (affects &quot;Play word&quot; speed): {pace}%
              </label>
              <input
                id="pace-slider"
                type="range"
                min={PACE_MIN}
                max={PACE_MAX}
                value={pace}
                onChange={(e) => setPace(Number(e.target.value))}
                className="mt-2 w-full accent-primary-500"
                aria-valuenow={pace}
                aria-valuemin={PACE_MIN}
                aria-valuemax={PACE_MAX}
              />
              <p className="mt-1 text-sm text-gray-500">Debounced value: {paceDebounced}%</p>
            </div>
          </>
        )}

        <form onSubmit={handleTextSubmit} className="flex gap-2">
          <input
            type="text"
            name="spoken"
            placeholder="Or type the word here..."
            className="flex-1 rounded-2xl border border-gray-300 bg-gray-50 px-4 py-3 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-200"
          />
          <Button type="submit" disabled={!wordId || loading}>
            Submit
          </Button>
        </form>

        {error && (
          <p className="text-sm text-red-600" role="alert">
            {error}
          </p>
        )}

        {result && (
          <div className="rounded-2xl border border-gray-200 bg-gray-50 p-4">
            <p className="text-sm font-medium text-gray-700">Transcript</p>
            <p className="mt-1 text-lg">
              Expected: <span className="font-semibold text-gray-900">{result.expected}</span>
            </p>
            <p className="mt-1 text-lg">
              You said:{" "}
              <span
                className={
                  result.is_correct
                    ? "font-semibold text-green-600"
                    : "font-semibold text-red-600"
                }
              >
                {result.recognized || "(empty)"}
              </span>
            </p>
            <p className="mt-2 text-sm text-gray-600">
              Score: {result.score}% · {result.is_correct ? "Correct" : "Incorrect"}
            </p>
          </div>
        )}
      </Card>
    </div>
  );
}
