"use client";

import { useState, useEffect, useRef } from "react";

/**
 * Debounces a value. Persists across re-renders; does not reset on re-render.
 * @param value - Value to debounce
 * @param delay - Delay in ms (e.g. 300)
 * @returns Debounced value
 */
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  const isFirstRender = useRef(true);
  const lastValue = useRef(value);

  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      setDebouncedValue(value);
      lastValue.current = value;
      return;
    }

    if (value === lastValue.current) return;
    lastValue.current = value;

    const timer = window.setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => window.clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
