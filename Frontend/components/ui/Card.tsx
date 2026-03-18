"use client";

import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: "none" | "sm" | "md" | "lg";
}

const paddingClasses = {
  none: "",
  sm: "p-4",
  md: "p-6",
  lg: "p-8",
};

export function Card({
  children,
  className = "",
  padding = "md",
}: CardProps) {
  return (
    <div
      className={`
        rounded-2xl bg-dyslexia-bg-primary shadow-soft border border-[#E8E4DC]
        transition-all duration-300 ease-out
        ${paddingClasses[padding]}
        ${className}
      `}
    >
      {children}
    </div>
  );
}
