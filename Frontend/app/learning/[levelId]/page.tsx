"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { learning, ApiError, type WordStatusOut } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { CompletionPopup } from "@/components/ui/CompletionPopup";
import { assetUrl } from "@/constants/assets";

export default function LevelWordsPage() {
  const router = useRouter();
  const params = useParams();
  const levelId = Number(params.levelId);
  const { token, checked } = useAuth();
  const [words, setWords] = useState<WordStatusOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showLevelCompletion, setShowLevelCompletion] = useState(false);

  useEffect(() => {
    if (!checked || !levelId) return;
    if (!token) {
      router.push("/auth/login");
      return;
    }
    learning
      .getWordsForLevel(levelId)
      .then((w) => {
        setWords(w);
        if (w.length > 0 && w.every((x) => x.is_mastered)) {
          setShowLevelCompletion(true);
        }
      })
      .catch((e) => {
        if (e instanceof ApiError && e.status === 403) {
          setError("Complete the previous level to unlock this one.");
        } else {
          setError(e instanceof ApiError ? e.message : "Failed to load words");
        }
      })
      .finally(() => setLoading(false));
  }, [levelId, token, checked, router]);

  if (!checked || !token) return null;
  if (loading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12">
        <p className="text-dyslexia-text-secondary leading-relaxed tracking-wide">Loading words…</p>
      </div>
    );
  }
  if (error) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12">
        <p className="text-dyslexia-accent-purple leading-relaxed tracking-wide">{error}</p>
        <Link href="/learning" className="mt-4 inline-block text-dyslexia-accent-blue hover:underline transition-colors duration-200">
          Back to levels
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6">
      <CompletionPopup
        open={showLevelCompletion}
        onClose={() => setShowLevelCompletion(false)}
        imageSrc={assetUrl("mainlevelcompletion.jpeg")}
        imageAlt="Level completed"
      >
        Hooray! Level completed
      </CompletionPopup>
      <div className="mb-8">
        <Link
          href="/learning"
          className="inline-flex items-center text-sm font-medium text-dyslexia-text-secondary hover:text-dyslexia-text-primary transition-all duration-200 leading-relaxed tracking-wide"
        >
          ← Back to levels
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-dyslexia-text-primary leading-relaxed tracking-wide">Level {levelId} words</h1>
        <p className="mt-1 text-dyslexia-text-secondary leading-relaxed tracking-wide">Practice these words.</p>
      </div>

      <div className="space-y-4">
        {words.map((w) => (
          <Card key={w.id} padding="md" className="transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-md">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-lg font-semibold text-dyslexia-text-primary leading-relaxed tracking-wide">{w.text}</p>
                {w.phonetics && (
                  <p className="text-sm text-dyslexia-text-secondary">{w.phonetics}</p>
                )}
                <p className="mt-1 text-sm text-dyslexia-text-secondary leading-relaxed tracking-wide">
                  Mastery: {Math.round(w.mastery_score * 100)}% 
                  {w.is_mastered && (
                    <span className="ml-2 text-dyslexia-accent-green">✓ Mastered</span>
                  )}
                </p>
              </div>
              <Link href={`/practice?wordId=${w.id}&levelId=${levelId}`}>
                <Button variant="secondary">Practice</Button>
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
