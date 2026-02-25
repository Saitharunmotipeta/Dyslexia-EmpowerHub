"use client";

import React from "react";

type Variant = "primary" | "secondary" | "outline" | "ghost" | "success";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  children: React.ReactNode;
  className?: string;
  loading?: boolean;
}

const variantClasses: Record<Variant, string> = {
  primary:
    "bg-primary-500 text-white hover:bg-primary-600 shadow-soft focus:ring-2 focus:ring-primary-400 focus:ring-offset-2",
  secondary:
    "bg-primary-100 text-primary-700 hover:bg-primary-200 focus:ring-2 focus:ring-primary-400 focus:ring-offset-2",
  outline:
    "bg-white border-2 border-primary-500 text-primary-600 hover:bg-primary-50 focus:ring-2 focus:ring-primary-400 focus:ring-offset-2",
  ghost:
    "bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-2 focus:ring-gray-300 focus:ring-offset-2",
  success:
    "bg-success-500 text-white hover:bg-success-600 shadow-soft focus:ring-2 focus:ring-success-400 focus:ring-offset-2",
};

export function Button({
  variant = "primary",
  children,
  className = "",
  loading = false,
  disabled,
  type = "button",
  ...props
}: ButtonProps) {
  return (
    <button
      type={type}
      className={`
        inline-flex items-center justify-center rounded-2xl px-5 py-2.5 text-base font-medium
        transition-colors disabled:opacity-50 disabled:cursor-not-allowed
        ${variantClasses[variant]}
        ${className}
      `}
      disabled={disabled || loading}
      aria-busy={loading}
      {...props}
    >
      {loading ? (
        <span className="inline-block h-5 w-5 animate-spin rounded-full border-2 border-current border-t-transparent" />
      ) : (
        children
      )}
    </button>
  );
}
