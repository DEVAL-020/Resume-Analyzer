import { useRef } from "react";
import type { MouseEvent, TouchEvent } from "react";

interface GradientSpotlightTextProps {
  text: string;
}

/**
 * Big outlined headline that reveals a purple-to-teal gradient fill
 * in a soft spotlight that follows the cursor. When there's no
 * pointer nearby the spotlight drifts on its own via CSS animation.
 */
export default function GradientSpotlightText({ text }: GradientSpotlightTextProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  function moveSpotlightTo(clientX: number, clientY: number) {
    const node = containerRef.current;
    if (!node) return;
    const rect = node.getBoundingClientRect();
    const x = ((clientX - rect.left) / rect.width) * 100;
    const y = ((clientY - rect.top) / rect.height) * 100;
    node.style.setProperty("--spot-x", `${x}%`);
    node.style.setProperty("--spot-y", `${y}%`);
    node.classList.add("is-hovering");
  }

  function handleMouseMove(e: MouseEvent<HTMLDivElement>) {
    moveSpotlightTo(e.clientX, e.clientY);
  }

  function handleTouchMove(e: TouchEvent<HTMLDivElement>) {
    const touch = e.touches[0];
    if (touch) moveSpotlightTo(touch.clientX, touch.clientY);
  }

  function handleLeave() {
    containerRef.current?.classList.remove("is-hovering");
  }

  return (
    <div
      ref={containerRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleLeave}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleLeave}
      className="spotlight-text-wrap relative select-none py-6"
      aria-hidden="true"
    >
      <span className="spotlight-text spotlight-text--base">{text}</span>
      <span className="spotlight-text spotlight-text--glow">{text}</span>

      <style>{`
        .spotlight-text-wrap {
          --spot-x: 50%;
          --spot-y: 50%;
        }

        .spotlight-text {
          display: block;
          width: 100%;
          text-align: center;
          font-family: 'Fraunces', serif;
          font-weight: 700;
          line-height: 1;
          white-space: nowrap;
          font-size: clamp(2.75rem, 12vw, 9rem);
        }

        .spotlight-text--base {
          color: transparent;
          -webkit-text-stroke: 1px rgb(var(--c-ink-faint) / 0.35);
          text-stroke: 1px rgb(var(--c-ink-faint) / 0.35);
        }

        .spotlight-text--glow {
          position: absolute;
          inset: 0;
          background: linear-gradient(120deg, #7C6CF0 0%, #7C6CF0 35%, #35C6A9 70%, #35C6A9 100%);
          background-clip: text;
          -webkit-background-clip: text;
          color: transparent;
          -webkit-mask-image: radial-gradient(circle 140px at var(--spot-x) var(--spot-y), black 0%, transparent 100%);
          mask-image: radial-gradient(circle 140px at var(--spot-x) var(--spot-y), black 0%, transparent 100%);
        }

        .spotlight-text-wrap {
          animation: driftSpotlight 9s ease-in-out infinite;
        }

        .spotlight-text-wrap.is-hovering {
          animation: none;
        }

        @keyframes driftSpotlight {
          0% { --spot-x: 12%; --spot-y: 30%; }
          25% { --spot-x: 38%; --spot-y: 70%; }
          50% { --spot-x: 62%; --spot-y: 25%; }
          75% { --spot-x: 85%; --spot-y: 65%; }
          100% { --spot-x: 12%; --spot-y: 30%; }
        }

        @media (prefers-reduced-motion: reduce) {
          .spotlight-text-wrap {
            animation: none;
          }
        }
      `}</style>
    </div>
  );
}
