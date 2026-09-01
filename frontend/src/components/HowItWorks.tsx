import Reveal from "./Reveal";

const STEPS = [
  {
    title: "Upload your resume",
    body: "PDF, DOCX, or plain text. The text is extracted and cleaned the same way the training data was.",
  },
  {
    title: "Add a job description",
    body: "Optional, but this is what turns a general category guess into a real fit check for one specific role.",
  },
  {
    title: "Read the breakdown",
    body: "See the predicted category with the words behind it, plus a fit score and exactly which required skills are missing.",
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="border-y border-paper-line bg-paper-card/60">
      <div className="mx-auto max-w-5xl px-6 py-16">
        <Reveal>
          <h2 className="font-display text-3xl font-semibold text-ink">How it works</h2>
        </Reveal>
        <div className="mt-10 grid grid-cols-1 gap-10 sm:grid-cols-3">
          {STEPS.map((step, i) => (
            <Reveal key={step.title} delay={i * 0.1}>
              <div className="flex h-9 w-9 items-center justify-center rounded-full border-2 border-ink bg-ink font-display text-sm font-semibold text-paper transition-transform duration-300 hover:scale-110">
                {i + 1}
              </div>
              <h3 className="mt-4 font-display text-lg font-semibold text-ink">
                {step.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-ink-soft">{step.body}</p>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
