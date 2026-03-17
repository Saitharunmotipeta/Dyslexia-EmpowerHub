"use client";

import React from "react";
import { Icon } from "./Icon";
import { ICON_NAMES } from "@/constants/icons";

interface PlaceholderMediaProps {
  type: "image" | "gif" | "audio";
  className?: string;
  label?: string;
}

export function PlaceholderMedia({
  type,
  className = "",
  label,
}: PlaceholderMediaProps) {
  const defaultLabels = {
    image: "Image placeholder",
    gif: "Animation placeholder",
    audio: "Audio placeholder",
  };
  const text = label ?? defaultLabels[type];

  const iconName = 
    type === "audio" ? ICON_NAMES.MUSIC : ICON_NAMES.IMAGE;

  return (
    <div
      className={`
        flex flex-col items-center justify-center rounded-2xl bg-gray-100 border-2 border-dashed border-gray-300
        min-h-[160px] text-gray-500
        ${className}
      `}
      aria-label={text}
    >
      <Icon name={iconName} size="xl" className="text-gray-400" />
      <span className="mt-2 text-sm font-medium">{text}</span>
    </div>
  );
}
