"use client";

import type { InsightBar } from "@/lib/profile-parse";

export function ProfileInsights({ bars }: { bars: InsightBar[] }) {
  return (
    <div className="space-y-4" aria-label="Learning insights">
      <h3 className="text-lg font-semibold text-dyslexia-text-primary">
        Insights & trends
      </h3>
      <p className="text-sm text-dyslexia-text-secondary leading-relaxed">
        These bars compare your activity to friendly targets (not grades). They update as you learn.
      </p>
      <ul className="space-y-3">
        {bars.map((b) => (
          <li key={b.label}>
            <div className="flex items-center justify-between gap-2 text-sm">
              <span className="font-medium text-dyslexia-text-primary">{b.label}</span>
              {b.hint && (
                <span className="text-dyslexia-text-secondary tabular-nums shrink-0">
                  {b.hint}
                </span>
              )}
            </div>
            <div
              className="mt-1 h-2.5 w-full overflow-hidden rounded-full bg-dyslexia-bg-secondary"
              role="progressbar"
              aria-valuenow={b.value}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-label={`${b.label}: ${b.value} percent of target`}
            >
              <div
                className="h-full rounded-full bg-gradient-to-r from-[#6B8CA3] to-[#4A6FA5] transition-all duration-500"
                style={{ width: `${b.value}%` }}
              />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
