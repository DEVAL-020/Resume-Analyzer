/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        paper: {
          DEFAULT: "rgb(var(--c-paper) / <alpha-value>)",
          card: "rgb(var(--c-paper-card) / <alpha-value>)",
          line: "rgb(var(--c-paper-line) / <alpha-value>)",
        },
        ink: {
          DEFAULT: "rgb(var(--c-ink) / <alpha-value>)",
          soft: "rgb(var(--c-ink-soft) / <alpha-value>)",
          faint: "rgb(var(--c-ink-faint) / <alpha-value>)",
        },
        highlighter: {
          DEFAULT: "rgb(var(--c-highlighter) / <alpha-value>)",
          soft: "rgb(var(--c-highlighter-soft) / <alpha-value>)",
          deep: "rgb(var(--c-highlighter-deep) / <alpha-value>)",
        },
        match: {
          DEFAULT: "rgb(var(--c-match) / <alpha-value>)",
          soft: "rgb(var(--c-match-soft) / <alpha-value>)",
        },
        gap: {
          DEFAULT: "rgb(var(--c-gap) / <alpha-value>)",
          soft: "rgb(var(--c-gap-soft) / <alpha-value>)",
        },
      },
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        body: ["'Work Sans'", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 0 rgb(var(--c-ink) / 0.06), 0 8px 24px -12px rgb(var(--c-ink) / 0.18)",
        "card-hover": "0 1px 0 rgb(var(--c-ink) / 0.08), 0 16px 32px -14px rgb(var(--c-ink) / 0.24)",
      },
      backgroundImage: {
        "highlight-stroke": "linear-gradient(105deg, transparent 0%, transparent 4%, #FFD23F 4%, #FFD23F 96%, transparent 96%)",
      },
      transitionTimingFunction: {
        "out-soft": "cubic-bezier(0.22, 1, 0.36, 1)",
      },
      keyframes: {
        fadeUp: {
          from: { opacity: "0", transform: "translateY(16px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        fadeUp: "fadeUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards",
      },
    },
  },
  plugins: [],
}
