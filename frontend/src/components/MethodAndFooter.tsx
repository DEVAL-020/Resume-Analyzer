import Reveal from "./Reveal";
import GradientSpotlightText from "./GradientSpotlightText";

export default function MethodAndFooter() {
  return (
    <>
      <section id="method" className="mx-auto max-w-5xl px-6 py-16">
        <Reveal>
          <h2 className="font-display text-3xl font-semibold text-ink">The two-layer design</h2>
        </Reveal>
        <div className="mt-8 grid grid-cols-1 gap-8 sm:grid-cols-2">
          <Reveal delay={0.05}>
            <div className="lift-on-hover h-full rounded-2xl border border-paper-line bg-paper-card p-6 hover:shadow-card-hover hover:border-ink-faint/40">
              <p className="text-sm font-medium text-highlighter-deep">Layer 1</p>
              <h3 className="mt-1 font-display text-xl font-semibold text-ink">
                Category prediction
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-ink-soft">
                A TF-IDF vectorizer and a classifier are trained on thousands
                of labeled resumes to learn which words and phrases associate
                with each job category — then the same model explains its own
                answer by surfacing the highest-weighted terms it found.
              </p>
            </div>
          </Reveal>
          <Reveal delay={0.15}>
            <div className="lift-on-hover h-full rounded-2xl border border-paper-line bg-paper-card p-6 hover:shadow-card-hover hover:border-ink-faint/40">
              <p className="text-sm font-medium text-match">Layer 2</p>
              <h3 className="mt-1 font-display text-xl font-semibold text-ink">
                Job-fit verification
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-ink-soft">
                A separate pass compares the resume directly against the job
                description: text similarity plus a skill-taxonomy overlap,
                so you see exactly which required skills are covered and
                which are missing — not just a category guess.
              </p>
            </div>
          </Reveal>
        </div>
      </section>

      <footer>
        <GradientSpotlightText text="Resume Analyzer" />  
        <div className="mx-auto max-w-5xl px-6 py-10">
          <p className="mt-6 text-sm text-ink-faint">
            Built as a part of a project for Python for Data Science Subject.
          </p>    

          <p className="mt-2 text-sm text-ink-faint">
            Copyright &copy; {new Date().getFullYear()} Resume Analyzer. All rights reserved. Made with ❤️ by <a href="https://www.linkedin.com/in/gecgce2024deval" target="_blank" style={{ color: "#494cfdff", textDecoration: "underline" }}>Deval Patel</a> and <a href="https://www.linkedin.com/in/gecgce24sujal" target="_blank" style={{ color: "#c01e1eff", textDecoration: "underline" }}>Sujal Patel</a>.
          </p>
        </div>

      </footer>
    </>
  );
}
