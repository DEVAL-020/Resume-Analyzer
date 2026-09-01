import { useState } from "react";
import { analyzeResume, ApiRequestError } from "../lib/api";
import type { AnalyzeResponse } from "../types";
import UploadDropzone from "./UploadDropzone";
import CategoryCard from "./CategoryCard";
import JobFitCard from "./JobFitCard";
import Reveal from "./Reveal";

export default function AnalyzerPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const canSubmit = file !== null && status !== "loading";

  async function handleSubmit() {
    if (!file) return;
    setStatus("loading");
    setErrorMessage("");
    try {
      const response = await analyzeResume(file, jobDescription);
      setResult(response);
      setStatus("idle");
    } catch (err) {
      const message =
        err instanceof ApiRequestError
          ? err.message
          : "Couldn't reach the analyzer. Is the backend running on port 8000?";
      setErrorMessage(message);
      setStatus("error");
    }
  }

  return (
    <section id="analyzer" className="mx-auto max-w-5xl px-6 py-16">
      <Reveal className="mb-10">
        <h2 className="font-display text-3xl font-semibold text-ink">Try it</h2>
        <p className="mt-2 max-w-xl text-ink-soft">
          Upload a resume and, optionally, paste the job description you're
          matching it against. Nothing is stored — analysis happens for this
          session only.
        </p>
      </Reveal>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
        <Reveal className="space-y-5">
          <UploadDropzone file={file} onFileSelected={setFile} />

          <div>
            <label htmlFor="jd" className="mb-2 block text-sm font-medium text-ink">
              Job description <span className="font-normal text-ink-faint">(optional)</span>
            </label>
            <textarea
              id="jd"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={8}
              placeholder="Paste the job posting here to get a fit score and skill-gap breakdown against this specific role..."
              className="w-full rounded-2xl border border-paper-line bg-paper-card p-4 text-sm text-ink placeholder:text-ink-faint transition-colors duration-300 focus:border-ink-faint"
            />
          </div>

          <button
            onClick={handleSubmit}
            disabled={!canSubmit}
            className="w-full rounded-full border-2 border-ink bg-ink px-6 py-3 font-medium text-paper transition-all duration-300 hover:-translate-y-0.5 hover:border-highlighter-deep hover:bg-ink/90 hover:shadow-card-hover disabled:cursor-not-allowed disabled:translate-y-0 disabled:border-paper-line disabled:opacity-40 disabled:shadow-none"
          >
            {status === "loading" ? "Analyzing..." : "Analyze resume"}
          </button>

          {status === "error" && (
            <p className="rounded-xl bg-gap-soft px-4 py-3 text-sm text-gap">{errorMessage}</p>
          )}
        </Reveal>

        <Reveal delay={0.1}>
          {result ? (
            <div className="space-y-6">
              <CategoryCard prediction={result.category_prediction} />
              {result.job_fit && <JobFitCard fit={result.job_fit} />}
              {!result.job_fit && (
                <p className="rounded-2xl border border-dashed border-paper-line p-6 text-sm text-ink-soft">
                  Add a job description on the left to see a fit score and
                  skill-gap breakdown for a specific role.
                </p>
              )}
            </div>
          ) : (
            <div className="flex h-full min-h-[300px] items-center justify-center rounded-2xl border border-dashed border-paper-line p-8 text-center">
              <p className="text-ink-faint">
                Results will appear here once you analyze a resume.
              </p>
            </div>
          )}
        </Reveal>
      </div>
    </section>
  );
}
