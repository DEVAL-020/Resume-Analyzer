import Reveal from "./Reveal";

export default function Hero() {
  return (
    <section id="top" className="mx-auto max-w-5xl px-6 pb-20 pt-8 sm:pt-16">
      <div className="grid grid-cols-1 items-center gap-12 lg:grid-cols-[1.1fr_1fr]">
        <Reveal>
          <h1 className="font-display text-4xl font-semibold leading-[1.1] text-ink sm:text-5xl">
            Know how your resume reads before a recruiter does.
          </h1>
          <p className="mt-5 max-w-md text-lg text-ink-soft">
            Upload a resume and a job description. A model trained on
            thousands of labeled resumes places it in a job category, then a
            second pass checks it word-for-word against the role you're
            actually applying for.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <a
              href="#analyzer"
              className="rounded-full border-2 border-ink bg-ink px-6 py-3 font-medium text-paper transition-all duration-300 hover:-translate-y-0.5 hover:border-highlighter-deep hover:bg-ink/90 hover:shadow-card-hover"
            >
              Analyze a resume
            </a>
            <a
              href="#how-it-works"
              className="rounded-full border-2 border-paper-line px-6 py-3 font-medium text-ink transition-all duration-300 hover:-translate-y-0.5 hover:border-ink-faint hover:shadow-card"
            >
              See how it works
            </a>
          </div>
        </Reveal>

        <Reveal delay={0.15} className="relative">
          <MockResumeCard />
        </Reveal>
      </div>
    </section>
  );
}

function MockResumeCard() {
  return (
    <div className="rounded-2xl border border-paper-line bg-paper-card p-7 shadow-card">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <div className="h-3 w-32 rounded bg-ink/80" />
          <div className="mt-2 h-2 w-20 rounded bg-ink-faint/50" />
        </div>
        <div className="rounded-full bg-match-soft px-3 py-1 text-xs font-medium text-match opacity-0 animate-[fadeIn_0.4s_ease_2.4s_forwards]">
          92% match
        </div>
      </div>

      <div className="space-y-2.5">
        <ResumeLine width="92%" delay={0} />
        <ResumeLine width="78%" delay={0.15} highlighted />
        <ResumeLine width="88%" delay={0.3} />
        <ResumeLine width="60%" delay={0.45} highlighted />
        <ResumeLine width="82%" delay={0.6} />
        <ResumeLine width="70%" delay={0.75} />
        <ResumeLine width="95%" delay={0.9} highlighted />
        <ResumeLine width="66%" delay={1.05} />
      </div>

      <div className="mt-6 flex flex-wrap gap-2">
        {["python", "sql", "aws"].map((skill, i) => (
          <span
            key={skill}
            className="inline-block translate-y-1 rounded-full border border-match/30 bg-match-soft px-3 py-1 text-xs font-medium text-match opacity-0"
            style={{
              animation: `chipIn 0.35s ease ${1.3 + i * 0.12}s forwards`,
            }}
          >
            {skill}
          </span>
        ))}
      </div>

      <style>{`
        @keyframes drawLine {
          from { transform: scaleX(0); }
          to { transform: scaleX(1); }
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(-2px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes chipIn {
          from { opacity: 0; transform: translateY(4px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}

function ResumeLine({
  width,
  delay,
  highlighted = false,
}: {
  width: string;
  delay: number;
  highlighted?: boolean;
}) {
  return (
    <div className="h-2.5 overflow-hidden rounded" style={{ width }}>
      <div
        className={`h-full origin-left rounded ${highlighted ? "bg-highlighter/70" : "bg-paper-line"
          }`}
        style={{
          transform: "scaleX(0)",
          animation: `drawLine 0.5s cubic-bezier(0.22,1,0.36,1) ${delay}s forwards`,
        }}
      />
    </div>
  );
}
