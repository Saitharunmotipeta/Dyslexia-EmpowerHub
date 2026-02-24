"use client";

import React from "react";

interface ProgressBarProps {
  value: number;
  max?: number;
  label?: string;
  variant?: "horizontal" | "vertical";
  className?: string;
}

export function ProgressBar({
  value,
  max = 100,
  label,
  variant = "horizontal",
  className = "",
}: ProgressBarProps) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));

  if (variant === "vertical") {
    return (
      <div className={`flex flex-col items-center gap-1 ${className}`}>
        <div
          className="w-8 rounded-2xl bg-gray-200 overflow-hidden flex flex-col justify-end"
          style={{ height: "80px" }}
          role="progressbar"
          aria-valuenow={value}
          aria-valuemin={0}
          aria-valuemax={max}
        >
          <div
            className="w-full rounded-2xl bg-primary-500 transition-all duration-300"
            style={{ height: `${pct}%`, minHeight: pct > 0 ? "4px" : 0 }}
          />
        </div>
        {label != null && (
          <span className="text-sm font-medium text-gray-600">{label}</span>
        )}
      </div>
    );
  }

  return (
    <div className={`w-full ${className}`}>
      <div
        className="h-3 w-full overflow-hidden rounded-2xl bg-gray-200"
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
      >
        <div
          className="h-full rounded-2xl bg-primary-500 transition-all duration-300"
          style={{ width: `${pct}%` }}
        />
      </div>
      {label != null && (
        <p className="mt-1 text-sm text-gray-600">{label}</p>
      )}
    </div>
  );
}
