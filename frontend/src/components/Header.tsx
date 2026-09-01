import { Moon, Sun } from "lucide-react";
import { useTheme } from "../hooks/useTheme";

export default function Header() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="mx-auto flex max-w-5xl items-center justify-between px-6 py-6">
      <a href="#top" className="flex items-center gap-2 transition-opacity duration-300 hover:opacity-80">
        <img src="/favicon.svg" width={50} height={50} alt="Resume Analyzer Logo" />
        <span className="font-display text-lg font-semibold text-ink">
          Resume Analyzer
        </span>
      </a>

      <div className="flex items-center gap-6">
        <nav className="hidden gap-6 text-sm text-ink-soft sm:flex">
          <a href="#how-it-works" className="nav-link">How it works</a>
          <a href="#analyzer" className="nav-link">Try it</a>
          <a href="#method" className="nav-link">Method</a>
        </nav>

        <button
          type="button"
          onClick={toggleTheme}
          aria-label={theme === "dark" ? "Switch to light theme" : "Switch to dark theme"}
          className="group relative flex h-10 w-10 items-center justify-center rounded-full border border-paper-line text-ink-soft transition-all duration-300 hover:border-ink-faint hover:text-ink hover:shadow-card"
        >
          <Sun
            size={18}
            className={`absolute transition-all duration-500 ${
              theme === "dark" ? "rotate-90 scale-0 opacity-0" : "rotate-0 scale-100 opacity-100"
            }`}
          />
          <Moon
            size={18}
            className={`absolute transition-all duration-500 ${
              theme === "dark" ? "rotate-0 scale-100 opacity-100" : "-rotate-90 scale-0 opacity-0"
            }`}
          />
        </button>
      </div>

      <style>{`
        .nav-link {
          position: relative;
          transition: color 0.3s ease;
          padding-bottom: 2px;
        }
        .nav-link::after {
          content: "";
          position: absolute;
          left: 0;
          bottom: 0;
          width: 100%;
          height: 1px;
          background-color: currentColor;
          transform: scaleX(0);
          transform-origin: right;
          transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
        }
        .nav-link:hover {
          color: rgb(var(--c-ink));
        }
        .nav-link:hover::after {
          transform: scaleX(1);
          transform-origin: left;
        }
      `}</style>
    </header>
  );
}
