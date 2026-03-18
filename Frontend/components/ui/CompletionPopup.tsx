"use client";

import { useEffect } from "react";
import { Icon } from "@/components/ui/Icon";
import { ICON_NAMES } from "@/constants/icons";

export interface CompletionPopupProps {
  open: boolean;
  onClose: () => void;
  imageSrc: string;
  imageAlt?: string;
  /** Visual variant only: "success" = soft glow, "retry" = minimal shake on appear */
  variant?: "success" | "retry";
  children: React.ReactNode;
}

/**
 * Reusable centered modal for completion/celebration popups.
 * Overlay background, close (X) top-right. Does not affect existing layout/logic.
 */
export function CompletionPopup({
  open,
  onClose,
  imageSrc,
  imageAlt = "Completion",
  variant,
  children,
}: CompletionPopupProps) {
  useEffect(() => {
    if (!open) return;
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleEscape);
    return () => window.removeEventListener("keydown", handleEscape);
  }, [open, onClose]);

  if (!open) return null;

  const modalGlow = variant === "success" ? "ring-2 ring-[#7FB77E]/30 shadow-[0_0_24px_rgba(127,183,126,0.15)]" : "";
  const innerShake = variant === "retry" ? "animate-shake-minimal [animation-delay:300ms]" : "";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="completion-popup-title"
    >
      {/* Overlay */}
      <button
        type="button"
        onClick={onClose}
        className="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity duration-300 ease-out"
        aria-label="Close"
      />
      {/* Modal box: scale 0.95→1, opacity 0→100, 300ms ease-out */}
      <div className={`relative z-10 w-full max-w-sm rounded-2xl border border-[#E8E4DC] bg-dyslexia-bg-primary p-6 shadow-xl animate-popup-in ${modalGlow}`}>
        <button
          type="button"
          onClick={onClose}
          className="absolute right-3 top-3 rounded-lg p-1 text-dyslexia-text-secondary hover:bg-dyslexia-bg-secondary hover:text-dyslexia-text-primary transition-all duration-200"
          aria-label="Close"
        >
          <Icon name={ICON_NAMES.CLOSE} size="base" />
        </button>
        <div className={`flex flex-col items-center text-center ${innerShake}`}>
          <img
            src={imageSrc}
            alt={imageAlt}
            className="mb-4 h-32 w-auto object-contain sm:h-40 rounded-xl shadow-sm transition-opacity duration-300"
          />
          <p id="completion-popup-title" className="text-lg font-semibold text-dyslexia-text-primary leading-relaxed tracking-wide">
            {children}
          </p>
        </div>
      </div>
    </div>
  );
}
