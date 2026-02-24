"use client";

import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  className?: string;
}

export function Input({
  label,
  error,
  className = "",
  id,
  ...props
}: InputProps) {
  const inputId = id ?? (label ? label.replace(/\s+/g, "-").toLowerCase() : undefined);
  return (
    <div className="w-full">
      {label && (
        <label
          htmlFor={inputId}
          className="mb-1.5 block text-sm font-medium text-gray-700"
        >
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={`
          w-full rounded-2xl border border-gray-300 bg-gray-50 px-4 py-3
          text-base text-gray-900 placeholder-gray-500
          focus:border-primary-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary-200
          disabled:opacity-60
          ${error ? "border-red-500 focus:border-red-500 focus:ring-red-100" : ""}
          ${className}
        `}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : undefined}
        {...props}
      />
      {error && (
        <p id={inputId ? `${inputId}-error` : undefined} className="mt-1 text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}
