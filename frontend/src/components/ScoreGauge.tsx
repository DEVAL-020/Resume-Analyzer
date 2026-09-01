interface ScoreGaugeProps {
  score: number;
  label: string;
}

const SIZE = 200;
const STROKE = 16;
const RADIUS = (SIZE - STROKE) / 2;
const CIRCUMFERENCE = Math.PI * RADIUS;

function bandColor(score: number): { track: string; text: string } {
  if (score >= 70) return { track: "#2F6F4E", text: "#2F6F4E" };
  if (score >= 40) return { track: "#E8B90F", text: "#8A6D00" };
  return { track: "#AE4A3A", text: "#AE4A3A" };
}

export default function ScoreGauge({ score, label }: ScoreGaugeProps) {
  const clamped = Math.max(0, Math.min(100, score));
  const offset = CIRCUMFERENCE - (clamped / 100) * CIRCUMFERENCE;
  const { track, text } = bandColor(clamped);
  const cx = SIZE / 2;
  const cy = SIZE / 2;

  return (
    <div className="flex flex-col items-center">
      <svg
        width={SIZE}
        height={SIZE / 2 + STROKE}
        viewBox={`0 0 ${SIZE} ${SIZE / 2 + STROKE}`}
        role="img"
        aria-label={`${label}: ${Math.round(clamped)} out of 100`}
      >
        <path
          d={`M ${STROKE / 2} ${cy} A ${RADIUS} ${RADIUS} 0 0 1 ${SIZE - STROKE / 2} ${cy}`}
          fill="none"
          stroke="rgb(var(--c-paper-line))"
          strokeWidth={STROKE}
          strokeLinecap="round"
        />
        <path
          d={`M ${STROKE / 2} ${cy} A ${RADIUS} ${RADIUS} 0 0 1 ${SIZE - STROKE / 2} ${cy}`}
          fill="none"
          stroke={track}
          strokeWidth={STROKE}
          strokeLinecap="round"
          strokeDasharray={CIRCUMFERENCE}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 900ms cubic-bezier(0.22, 1, 0.36, 1), stroke 0.4s ease" }}
        />
        <text
          x={cx}
          y={cy - 6}
          textAnchor="middle"
          className="font-display"
          style={{ fontSize: 40, fontWeight: 600, fill: text }}
        >
          {Math.round(clamped)}
        </text>
        <text
          x={cx}
          y={cy + 16}
          textAnchor="middle"
          style={{ fontSize: 12, fill: "rgb(var(--c-ink-soft))" }}
        >
          out of 100
        </text>
      </svg>
      <p className="mt-1 text-sm font-medium text-ink-soft">{label}</p>
    </div>
  );
}
