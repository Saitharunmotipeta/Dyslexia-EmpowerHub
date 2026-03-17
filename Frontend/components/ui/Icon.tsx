"use client";

import React from "react";
import * as LucideIcons from "lucide-react";

export type IconSize = "sm" | "base" | "lg" | "xl";

interface IconProps {
  name: keyof typeof LucideIcons;
  size?: IconSize;
  className?: string;
  /** Icon name mapped via ICON_NAMES constant (e.g., "checkCircle", "menu") */
}

const sizeMap: Record<IconSize, string> = {
  sm: "w-4 h-4",
  base: "w-5 h-5",
  lg: "w-6 h-6",
  xl: "w-8 h-8",
};

/**
 * Icon wrapper component for Lucide React icons.
 * Provides semantic sizing and dark mode support (inherits text color).
 * 
 * Usage:
 * ```tsx
 * <Icon name="CheckCircle2" size="base" />
 * <Icon name="Menu" className="text-primary-600" />
 * ```
 */
export function Icon({ name, size = "base", className = "" }: IconProps) {
  const IconComponent = LucideIcons[name] as React.ComponentType<{
    className?: string;
  }>;

  if (!IconComponent) {
    console.warn(`Icon "${name}" not found in lucide-react`);
    return null;
  }

  return (
    <IconComponent
      className={`${sizeMap[size]} ${className}`}
      aria-hidden="true"
    />
  );
}
