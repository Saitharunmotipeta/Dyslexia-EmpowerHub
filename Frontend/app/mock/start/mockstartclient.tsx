"use client";

export const dynamic = "force-dynamic";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { type MockStartResponse } from "@/lib/api";
import { useMediaRecorder } from "@/hooks/useMediaRecorder";
import { getPublicApiBaseUrl } from "@/lib/apiBase";
import { evaluatePracticeAudio } from "@/lib/speech/evaluatePracticeAudio";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { PlaceholderMedia } from "@/components/ui/PlaceholderMedia";
import { assetUrl } from "@/constants/assets";

const API = getPublicApiBaseUrl();

const getImageWithFallback = (wordKey: string) => {
  return [assetUrl(`${wordKey}.jpg`), assetUrl(`${wordKey}.png`)];
};

export default function MockRunPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const levelIdParam = searchParams.get("levelId");
  const levelId = levelIdParam ? parseInt(levelIdParam, 10) : null;
  const [imgError, setImgError] = useState(false);
  const [imgIndex, setImgIndex] = useState(0);

  const { token, checked } = useAuth();
  const [data, setData] = useState<MockStartResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [submittingStage, setSubmittingStage] = useState<string | null>(null);
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
    if (!token) {
      router.push("/auth/login");
      return;
    }
    if (!levelId) {
      setError("Missing level. Go back and choose a level.");
      setLoading(false);
      return;
    }

    (async () => {
      try {
        const res = await fetch(`${API}/mock/start?level_id=${levelId}`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) throw new Error(await res.text());
        setData((await res.json()) as MockStartResponse);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to start mock");
      } finally {
        setLoading(false);
      }
    })();
  }, [levelId, token, checked, router]);

  const currentWord = data?.words?.[currentIndex];
  const isLast = data && currentIndex >= data.words.length - 1;

  useEffect(() => {
    if (!micError) return;
    setError(micError);
  }, [micError]);

  useEffect(() => {
    // New word: clear previous recording
    reset();
  }, [currentIndex, reset]);

  useEffect(() => {
    setImgError(false);
    setImgIndex(0);
  }, [currentIndex]);

  const handleSubmitWord = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!data || !currentWord) return;
    if (!token) {
      setError("Not authenticated.");
      return;
    }
    setSubmitting(true);
    setSubmittingStage("Uploading recording...");
    try {
      if (!audioBlob || audioBlob.size === 0) {
        setError("Recording was empty. Tap Record, speak, then Stop, and try again.");
        return;
      }

      // -----------------------------
      // STEP 1: EVALUATE (audio → recognized)
      // -----------------------------
      const evalData = await evaluatePracticeAudio({
        token,
        wordId: currentWord.id,
        audioBlob,
        apiBaseUrl: API,
      });
      setSubmittingStage("Analyzing pronunciation...");

      // -----------------------------
      // STEP 2: Submit recognized → /mock/word
      // -----------------------------
      const res = await fetch(`${API}/mock/word`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          public_attempt_id: data.public_attempt_id,
          word_id: currentWord.id,
          spoken: evalData.recognized,
        }),
      });

      if (!res.ok) throw new Error(await res.text());
      setSubmittingStage("Saving answer...");

      if (isLast) {
        router.push(`/mock/result?public_attempt_id=${encodeURIComponent(data.public_attempt_id)}`);
        return;
      }
      setCurrentIndex((i) => i + 1);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Submit failed");
    } finally {
      setSubmitting(false);
      setSubmittingStage(null);
    }
  };

  // Hear word (TTS)
  const playWord = useCallback(() => {
    const word = currentWord?.word;
    if (!word || typeof window === "undefined" || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(word);
    u.lang = "en-US";
    window.speechSynthesis.speak(u);
  }, [currentWord?.word]);

  if (!checked || !token) return null;
  if (loading) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-gray-600">Starting mock test…</p>
      </div>
    );
  }
  if (error && !data) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-red-600">{error}</p>
        <Button variant="outline" className="mt-4" onClick={() => router.push("/mock")}>
          Back to levels
        </Button>
      </div>
    );
  }
  if (!data) return null;

  const wordKey = currentWord?.word
    ?.toLowerCase()
    .trim()
    .replace(/\s+/g, "");

  const imageCandidates = wordKey ? getImageWithFallback(wordKey) : [];

  const currentWithImage = currentWord as typeof currentWord & { image_url?: string };
  const finalImage =
    currentWithImage?.image_url && currentWithImage.image_url.trim() !== "" && !imgError
      ? currentWithImage.image_url
      : imageCandidates[imgIndex];

  return (
    <div className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
      <div className="mb-4">
        <Link href="/mock" className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900">
          ← Back to mock levels
        </Link>
      </div>
      <div className="mb-6 flex items-center justify-between">
        <span className="text-sm text-gray-600">
          Word {currentIndex + 1} of {data.words.length}
        </span>
      </div>

      <Card className="space-y-6" padding="lg">
      <div className="min-h-[160px] overflow-hidden rounded-xl bg-gray-100">
      {finalImage ? (
        <img
          src={finalImage}
          alt={currentWord?.word}
          className="h-full w-full object-contain rounded-xl"
          onError={() => {
            if (imgIndex < imageCandidates.length - 1) {
              setImgIndex((prev) => prev + 1);
            } else {
              setImgError(true);
            }
          }}
        />
      ) : (
        <PlaceholderMedia type="image" label="Word image" />
      )}
    </div>
        <p className="text-center text-2xl font-bold text-gray-900">
          {currentWord?.word ?? "—"}
        </p>

        <div className="flex flex-wrap items-center gap-3">
          <Button
            type="button"
            variant="outline"
            onClick={playWord}
            disabled={!currentWord?.word}
            aria-label="Hear word"
          >
            <span className="mr-2" aria-hidden>🔊</span>
            Hear word
          </Button>
          <Button
            type="button"
            variant={recording ? "secondary" : "primary"}
            onClick={recording ? stopRecording : startRecording}
            disabled={!currentWord}
            aria-pressed={recording}
          >
            {recording ? "Stop" : "🎙 Record"}
          </Button>
        </div>

        <form onSubmit={handleSubmitWord} className="space-y-4">
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

          <Button type="submit" disabled={submitting || !audioBlob} className="w-full">
            {isLast ? "Finish test" : "Next word"}
          </Button>
        </form>

        {error && (
          <p className="text-sm text-red-600" role="alert">
            {error}
          </p>
        )}
        {submitting && submittingStage && (
          <p className="text-sm text-gray-600" role="status">
            {submittingStage}
          </p>
        )}
      </Card>
    </div>
  );
}
