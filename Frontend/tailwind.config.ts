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
      },
      fontFamily: {
        sans: ["var(--font-open-dyslexic)", "system-ui", "sans-serif"],
      },
      borderRadius: { "2xl": "1rem" },
      boxShadow: {
        soft: "0 4px 14px 0 rgba(0, 0, 0, 0.06)",
        "soft-lg": "0 10px 40px -10px rgba(0, 0, 0, 0.08)",
      },
    },
  },
  plugins: [],
};

export default config;
