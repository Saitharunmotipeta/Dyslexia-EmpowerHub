/**
 * API client for Dyslexia Backend.
 * Base URL from NEXT_PUBLIC_API_BASE_URL. All routes match backend exactly.
 */

const getBaseUrl = () => {
  const url = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!url) throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  return url.replace(/\/$/, "");
};

const getToken = (): string | null => {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
};

type RequestInitWithBody = RequestInit & { body?: object };

async function request<T>(
  path: string,
  options: RequestInitWithBody = {}
): Promise<T> {
  const base = getBaseUrl();
  const url = path.startsWith("http") ? path : `${base}${path}`;
  const token = getToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const init: RequestInit = {
    ...options,
    headers,
    body:
      options.body !== undefined
        ? typeof options.body === "string"
          ? options.body
          : JSON.stringify(options.body)
        : undefined,
  };

  const res = await fetch(url, init);
  if (!res.ok) {
    const text = await res.text();
    let detail: string;
    try {
      const j = JSON.parse(text);
      detail = j.detail ?? (typeof j.detail === "object" ? JSON.stringify(j.detail) : text);
    } catch {
      detail = text || res.statusText;
    }
    throw new ApiError(res.status, detail);
  }

  const contentType = res.headers.get("content-type");
  if (contentType?.includes("application/json")) {
    return res.json() as Promise<T>;
  }
  return res.text() as Promise<T>;
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

// ─── Auth ─────────────────────────────────────────────────────────────────
export interface RegisterIn {
  username: string;
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: number;
  streak_days: number;
  total_login_days: number;
}

export interface ProfileResponse {
  id: number;
  name: string;
  email: string;
  role: string;
  streak_days: number;
  total_login_days: number;
  points: number;
  total_time_spent: number;
  courses_completed: number;
  badges: string;
  achievements: string;
}

export const auth = {
  register: (data: RegisterIn) =>
    request<{ message: string; user_id: number }>("/auth/register", {
      method: "POST",
      body: data,
    }),

  login: (email: string, password: string) => {
    const form = new URLSearchParams();
    form.set("username", email);
    form.set("password", password);
    const base = getBaseUrl();
    const token = getToken();
    const headers: HeadersInit = {
      "Content-Type": "application/x-www-form-urlencoded",
    };
    if (token) (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
    return fetch(`${base}/auth/login`, {
      method: "POST",
      headers,
      body: form.toString(),
    }).then(async (res) => {
      if (!res.ok) {
        const text = await res.text();
        let detail: string;
        try {
          const j = JSON.parse(text);
          detail = j.detail ?? text;
        } catch {
          detail = text || res.statusText;
        }
        throw new ApiError(res.status, detail);
      }
      return res.json() as Promise<LoginResponse>;
    });
  },

  profile: () =>
    request<ProfileResponse>("/auth/profile", { method: "GET" }),
};

// ─── Learning ──────────────────────────────────────────────────────────────
export interface LevelOut {
  id: number;
  name: string;
  description: string;
  difficulty: string;
  order: number;
  total_words: number;
  mastered_words: number;
  mastered_percentage: number;
  is_unlocked: boolean;
}

export interface WordStatusOut {
  id: number;
  text: string;
  phonetics: string;
  syllables: string;
  difficulty: string;
  image_url?: string | null;
  is_mastered: boolean;
  mastery_score: number;
  attempts: number;
}

export const learning = {
  getLevels: () =>
    request<LevelOut[]>("/learning/levels", { method: "GET" }),

  getWordsForLevel: (levelId: number) =>
    request<WordStatusOut[]>(`/learning/levels/${levelId}/words`, {
      method: "GET",
    }),

  updateWordStatus: (
    wordId: number,
    isMastered: boolean,
    masteryScore: number
  ) =>
    request<{ message: string; word_id: number; is_mastered: boolean; mastery_score: number }>(
      `/learning/words/${wordId}/update_status`,
      {
        method: "POST",
        body: { is_mastered: isMastered, mastery_score: masteryScore },
      }
    ),
};

// ─── Practice ─────────────────────────────────────────────────────────────
export interface EvaluationRequest {
  word_id: number;
  recognized_text: string;
}

export interface EvaluationResponse {
  word_id: number;
  expected: string;
  recognized: string;
  score: number;
  verdict?: string;
  is_correct: boolean;
}

export interface PracticeAutoIn {
  word_id: number;
  pace: number;
  level_id: number;
  spoken: string;
}

export interface PhonemeResponse {
  status: string;
  input: string;
  phonemes: string;
}

export const practice = {
  evaluate: (payload: EvaluationRequest) =>
    request<EvaluationResponse>("/practice/evaluate", {
      method: "POST",
      body: payload,
    }),

  auto: (payload: PracticeAutoIn) =>
    request<{ status: string; data: unknown }>("/practice/auto", {
      method: "POST",
      body: payload,
    }),

  phoneme: (text: string) =>
    request<PhonemeResponse>("/practice/phoneme", {
      method: "POST",
      body: { text },
    }),
};

// ─── Feedback (Insights) ──────────────────────────────────────────────────
export interface FeedbackIn {
  mode: "static" | "dynamic";
  content_type: "word" | "phrase" | "sentence";
  text: string;
  spoken: string;
  score: number;
  attempts: number;
  pace?: number;
}

export interface RecommendationOut {
  recommendation: string;
  headline: string;
  explanation: string;
  confidence: number;
  next_steps: string[];
  metrics_used?: Record<string, unknown>;
}

export const feedback = {
  trend: (data: FeedbackIn) =>
    request<{ trend: unknown }>("/feedback/trend", {
      method: "POST",
      body: data,
    }),

  pattern: (data: FeedbackIn) =>
    request<{ pattern: unknown }>("/feedback/pattern", {
      method: "POST",
      body: data,
    }),

  generate: (data: FeedbackIn) =>
    request<unknown>("/feedback/generate", {
      method: "POST",
      body: data,
    }),

  recommendation: (data: FeedbackIn) =>
    request<RecommendationOut>("/feedback/recommendation", {
      method: "POST",
      body: data,
    }),

  aggregate: (data: FeedbackIn) =>
    request<{
      trend: unknown;
      pattern: unknown;
      feedback: unknown;
      recommendation: RecommendationOut;
    }>("/feedback/aggregate", {
      method: "POST",
      body: data,
    }),
};

// ─── Mock ─────────────────────────────────────────────────────────────────
export interface MockWord {
  id: number;
  word: string;
}

export interface MockStartResponse {
  public_attempt_id: string;
  words: MockWord[];
  message: string;
}

export interface MockWordRequest {
  public_attempt_id: string;
  word_id: number;
  spoken: string;
}

export interface MockWordResponse {
  word_id: number;
  public_attempt_id: string;
  spoken: string;
  score: number;
  verdict: string;
  message: string;
  recognized_text: string;
}

export interface MockResultRequest {
  public_attempt_id: string;
}

export interface MockResultResponse {
  public_attempt_id: string;
  score: number;
  verdict: string;
  words: Array<Record<string, unknown>>;
  message: string;
  recommendations: Array<Record<string, unknown>>;
  confidence: number;
  metrics: Record<string, number>;
  tips: string[];
  next_steps: string[];
  detailed_feedback: Array<Record<string, unknown>>;
}

export const mock = {
  start: (levelId: number) =>
    request<MockStartResponse>(`/mock/start?level_id=${levelId}`, {
      method: "POST",
    }),

  submitWord: (payload: MockWordRequest) =>
    request<MockWordResponse>("/mock/word", {
      method: "POST",
      body: payload,
    }),

  getResult: (payload: MockResultRequest) =>
    request<MockResultResponse>("/mock/result", {
      method: "POST",
      body: payload,
    }),

  report: (publicAttemptId: string) =>
    request<{
      attempt_id: string;
      final_score: number;
      verdict: string;
      words: Array<Record<string, unknown>>;
      pdf_generated: boolean;
      message: string;
    }>(`/mock/report?public_attempt_id=${encodeURIComponent(publicAttemptId)}`, {
      method: "POST",
    }),
};

// ─── Dynamic ──────────────────────────────────────────────────────────────
export interface DynamicAnalyzeIn {
  text: string;
}

export interface DynamicAnalyzeOut {
  type: "word" | "sentence";
  words: string[];
  meaning: string;
}

export interface DynamicAttemptCreate {
  text: string;
  text_type: "word" | "sentence";
  spoken: string;
  score: number;
  pace?: number;
}

export interface DynamicAttemptOut {
  attempt_id: string;
  message: string;
}

export const dynamicApi = {
  analyze: (data: DynamicAnalyzeIn) =>
    request<DynamicAnalyzeOut>("/dynamic/analyze", {
      method: "POST",
      body: data,
    }),

  attempt: (data: DynamicAttemptCreate) =>
    request<DynamicAttemptOut>("/dynamic/attempt", {
      method: "POST",
      body: data,
    }),
};

// ─── Chatbot ───────────────────────────────────────────────────────────────
export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  reply: string;
  mode: string;
  llm_used: boolean;
}

export const chatbot = {
  chat: (payload: ChatRequest) =>
    request<ChatResponse>("/chatbot/chat", {
      method: "POST",
      body: payload,
    }),
};

// Health (no auth)
export const health = () =>
  request<{ status: string }>("/", { method: "GET" });
