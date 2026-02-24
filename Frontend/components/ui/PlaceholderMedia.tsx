"use client";

import React from "react";

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

  const icon =
    type === "audio" ? (
      <svg className="h-12 w-12 text-gray-400" fill="currentColor" viewBox="0 0 24 24" aria-hidden>
        <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z" />
      </svg>
    ) : (
      <svg className="h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden>
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14" />
      </svg>
    );

  return (
    <div
      className={`
        flex flex-col items-center justify-center rounded-2xl bg-gray-100 border-2 border-dashed border-gray-300
        min-h-[160px] text-gray-500
        ${className}
      `}
      aria-label={text}
    >
      {icon}
      <span className="mt-2 text-sm font-medium">{text}</span>
    </div>
  );
}
