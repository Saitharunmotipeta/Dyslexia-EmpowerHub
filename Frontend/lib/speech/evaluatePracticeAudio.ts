import { getPublicApiBaseUrl } from "@/lib/apiBase";

function filenameForAudioBlob(blob: Blob): string {
  const t = blob.type || "";
  if (t.includes("mp4") || t.includes("m4a")) return "audio.m4a";
  if (t.includes("ogg")) return "audio.ogg";
  return "audio.webm";
}

export type PracticeEvaluation = {
  word_id: number;
  expected: string;
  recognized: string;
  score: number;
  verdict?: string;
  is_correct: boolean;
};

export async function parseApiErrorMessage(res: Response): Promise<string> {
  const text = await res.text();
  try {
    const j = JSON.parse(text) as { detail?: unknown };
    if (typeof j.detail === "string") return j.detail;

    if (Array.isArray(j.detail)) {
      const msgs = j.detail
        .map((d: { msg?: string }) => d.msg)
        .filter((m): m is string => Boolean(m));
      if (msgs.length) return msgs.join("; ");
    }
  } catch {}

  return text.trim() || `Request failed (${res.status})`;
}

/* ================= PRACTICE (OLD FLOW) ================= */
export async function evaluatePracticeAudio(params: {
  token: string;
  wordId: number;
  audioBlob: Blob;
  apiBaseUrl?: string;
}): Promise<PracticeEvaluation> {
  const { token, wordId, audioBlob, apiBaseUrl } = params;
  const API = apiBaseUrl ?? getPublicApiBaseUrl();

  const formData = new FormData();
  formData.append("word_id", String(wordId));
  formData.append("file", audioBlob, filenameForAudioBlob(audioBlob));

  const res = await fetch(`${API}/practice/evaluate`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!res.ok) {
    throw new Error(await parseApiErrorMessage(res));
  }

  return (await res.json()) as PracticeEvaluation;
}

/* ================= DYNAMIC (FIXED VERSION) ================= */
export async function evaluateDynamicAudio(params: {
  token: string;
  expectedText: string;
  audioBlob: Blob;
  apiBaseUrl?: string;
}): Promise<PracticeEvaluation> {
  const { token, expectedText, audioBlob, apiBaseUrl } = params;
  const API = apiBaseUrl ?? getPublicApiBaseUrl();

  const formData = new FormData();
  formData.append("expected_text", expectedText.trim());
  formData.append("file", audioBlob, filenameForAudioBlob(audioBlob));

  const res = await fetch(`${API}/dynamic/evaluate-audio`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`, // ✅ only this
    },
    body: formData, // ✅ IMPORTANT: no JSON
  });

  if (!res.ok) {
    throw new Error(await parseApiErrorMessage(res));
  }

  return (await res.json()) as PracticeEvaluation;
}