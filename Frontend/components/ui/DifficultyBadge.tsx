"use client";

import React from "react";
import { Icon } from "./Icon";
import { ICON_NAMES } from "@/constants/icons";

type Difficulty = "easy" | "medium" | "hard" | string;

const difficultyStyles: Record<string, { style: string; icon: string }> = {
  easy: { style: "bg-success-500 text-white", icon: ICON_NAMES.LIGHTBULB },
  medium: { style: "bg-primary-500 text-white", icon: ICON_NAMES.FLAME },
  hard: { style: "bg-warning-500 text-white", icon: ICON_NAMES.ZAPS },
};

export function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
  const key = difficulty.toLowerCase();
  const config = difficultyStyles[key] ?? { style: "bg-gray-500 text-white", icon: ICON_NAMES.TARGET };

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-xl px-3 py-1 text-sm font-medium ${config.style}`}
    >
      <Icon name={config.icon as any} size="sm" />
      {difficulty}
    </span>
  );
}
