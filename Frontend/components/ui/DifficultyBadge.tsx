"use client";

import React from "react";

type Difficulty = "easy" | "medium" | "hard" | string;

const difficultyStyles: Record<string, string> = {
  easy: "bg-success-500 text-white",
  medium: "bg-primary-500 text-white",
  hard: "bg-warning-500 text-white",
};

export function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
  const key = difficulty.toLowerCase();
  const style = difficultyStyles[key] ?? "bg-gray-500 text-white";

  return (
    <span
      className={`inline-block rounded-xl px-3 py-1 text-sm font-medium ${style}`}
    >
      {difficulty}
    </span>
  );
}
