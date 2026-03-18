import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eef9ff",
          100: "#d9f1ff",
          200: "#bce7ff",
          300: "#8ed9ff",
          400: "#59c2ff",
          500: "#33a6ff",
          600: "#1a87f5",
          700: "#146ee1",
          800: "#1758b6",
          900: "#194b8f",
        },
        success: { 500: "#22c55e", 600: "#16a34a" },
        warning: { 500: "#f59e0b", 600: "#d97706" },
        /* Dyslexia-friendly palette (soft, calm) */
        dyslexia: {
          "bg-primary": "#FFF8E7",
          "bg-secondary": "#F4F4F4",
          "text-primary": "#1A1A1A",
          "text-secondary": "#333333",
          "accent-blue": "#6B8CA3",
          "accent-green": "#7FB77E",
          "accent-purple": "#A78BFA",
        },
      },
      fontFamily: {
        sans: ["var(--font-open-dyslexic)", "system-ui", "sans-serif"],
      },
      borderRadius: { "2xl": "1rem" },
      boxShadow: {
        soft: "0 4px 14px 0 rgba(0, 0, 0, 0.06)",
        "soft-lg": "0 10px 40px -10px rgba(0, 0, 0, 0.08)",
      },
      keyframes: {
        "popup-in": {
          "0%": { opacity: "0", transform: "scale(0.95)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        "shake-minimal": {
          "0%, 100%": { transform: "translateX(0)" },
          "25%": { transform: "translateX(-2px)" },
          "75%": { transform: "translateX(2px)" },
        },
        "fade-rise": {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        "popup-in": "popup-in 300ms ease-out forwards",
        "shake-minimal": "shake-minimal 300ms ease-out",
        "fade-rise": "fade-rise 300ms ease-out forwards",
      },
    },
  },
  plugins: [],
};

export default config;
