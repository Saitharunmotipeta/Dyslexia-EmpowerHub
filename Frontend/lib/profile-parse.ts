/** Parse badges/achievements stored as JSON array or comma-separated string. */
export function parseStoredList(raw: string | null | undefined): string[] {
  if (raw == null || raw === "") return [];
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (Array.isArray(parsed)) {
      return parsed.map(String).map((s) => s.trim()).filter(Boolean);
    }
  } catch {
    /* fall through */
  }
  return raw
    .split(",")
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
}

const PRETTY: Record<string, string> = {
  first_login: "First login",
  streak_7: "7-day streak",
  streak_30: "30-day streak",
  level_master: "Level master",
  mock_star: "Mock test star",
};

export function formatBadgeLabel(code: string): string {
  return PRETTY[code] ?? code.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

/** Heuristic engagement score from profile fields (0–100), for UI only. */
export function engagementPercent(input: {
  streak_days: number;
  total_login_days: number;
  total_time_spent: number;
  points: number;
  courses_completed: number;
}): number {
  const streak = Math.min(100, (input.streak_days / 30) * 100);
  const logins = Math.min(100, (input.total_login_days / 45) * 100);
  const hours = input.total_time_spent / 3600;
  const time = Math.min(100, (hours / 12) * 100);
  const levels = Math.min(100, input.courses_completed * 12);
  const pts = Math.min(100, (input.points / 1500) * 100);
  return Math.round((streak + logins + time + levels + pts) / 5);
}

export type InsightBar = { label: string; value: number; hint?: string };

export function profileInsightBars(input: {
  streak_days: number;
  total_login_days: number;
  total_time_spent: number;
  points: number;
  courses_completed: number;
}): InsightBar[] {
  const hours = input.total_time_spent / 3600;
  return [
    {
      label: "Streak",
      value: Math.min(100, Math.round((input.streak_days / 30) * 100)),
      hint: `${input.streak_days} days`,
    },
    {
      label: "Login habit",
      value: Math.min(100, Math.round((input.total_login_days / 60) * 100)),
      hint: `${input.total_login_days} days`,
    },
    {
      label: "Study time",
      value: Math.min(100, Math.round((hours / 15) * 100)),
      hint: `${hours.toFixed(1)} h total`,
    },
    {
      label: "Levels",
      value: Math.min(100, input.courses_completed * 15),
      hint: `${input.courses_completed} completed`,
    },
    {
      label: "Points",
      value: Math.min(100, Math.round((input.points / 2000) * 100)),
      hint: input.points.toLocaleString(),
    },
  ];
}
