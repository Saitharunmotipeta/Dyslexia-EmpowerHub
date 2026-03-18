"use client";

import React, { useEffect, useState } from "react";

const STORAGE_KEY = "dyslexiaMode";
const BODY_CLASS = "dyslexia-mode";

function getStored(): boolean {
  if (typeof window === "undefined") return false;
  try {
    return localStorage.getItem(STORAGE_KEY) === "true";
  } catch {
    return false;
  }
}

function setStored(value: boolean): void {
  try {
    if (value) localStorage.setItem(STORAGE_KEY, "true");
    else localStorage.removeItem(STORAGE_KEY);
  } catch {}
}

export function DyslexiaModeToggle() {
  const [on, setOn] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const value = getStored();
    setOn(value);
    if (value) document.body.classList.add(BODY_CLASS);
    setMounted(true);
  }, []);

  function handleToggle() {
    const next = !on;
    setOn(next);
    setStored(next);
    if (next) document.body.classList.add(BODY_CLASS);
    else document.body.classList.remove(BODY_CLASS);
  }

  if (!mounted) return null;

  return (
    <div
      className="fixed bottom-5 right-5 z-[9999] flex items-center gap-2 rounded-full bg-dyslexia-bg-primary px-3 py-2 shadow-soft-lg ring-1 ring-[#E8E4DC] transition-all duration-300 ease-out"
      role="region"
      aria-label="Dyslexia-friendly reading mode"
    >
      <span className="whitespace-nowrap text-sm font-medium text-dyslexia-text-primary leading-relaxed tracking-wide">
        Reading mode
      </span>
      <button
        type="button"
        role="switch"
        aria-checked={on}
        aria-label={on ? "Turn off dyslexia-friendly reading mode" : "Turn on dyslexia-friendly reading mode"}
        onClick={handleToggle}
        className={`relative h-6 w-11 shrink-0 rounded-full transition-all duration-300 ease-out focus:outline-none focus:ring-2 focus:ring-dyslexia-accent-blue focus:ring-offset-2 ${
          on ? "bg-dyslexia-accent-blue" : "bg-[#E8E4DC]"
        }`}
        style={{ padding: 0 }}
      >
        <span
          className={`pointer-events-none absolute top-1 h-4 w-4 rounded-full bg-white shadow transition-transform ${
            on ? "left-6" : "left-1"
          }`}
          aria-hidden
        />
      </button>
    </div>
  );
}
