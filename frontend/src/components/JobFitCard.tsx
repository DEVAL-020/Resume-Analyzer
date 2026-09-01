import type { JobFit } from "../types";
import ScoreGauge from "./ScoreGauge";
import SkillChips from "./SkillChips";

export default function JobFitCard({ fit }: { fit: JobFit }) {
  return (
    <div className="lift-on-hover rounded-2xl border border-paper-line bg-paper-card p-6 shadow-card hover:border-ink-faint/40 hover:shadow-card-hover">
      <h3 className="font-display text-lg font-semibold text-ink">Fit for this role</h3>

      <div className="mt-4 grid grid-cols-1 gap-6 sm:grid-cols-[auto_1fr] sm:items-center">
        <ScoreGauge score={fit.fit_score} label="Overall fit score" />
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-2xl font-semibold text-ink">{Math.round(fit.text_similarity_pct)}%</p>
            <p className="text-sm text-ink-soft">Text similarity to the job description</p>
          </div>
          <div>
            <p className="text-2xl font-semibold text-ink">{Math.round(fit.skill_coverage_pct)}%</p>
            <p className="text-sm text-ink-soft">Required skills covered</p>
          </div>
        </div>
      </div>

      <div className="mt-6 space-y-5 border-t border-paper-line pt-5">
        <div>
          <p className="mb-2 text-sm font-medium text-ink">
            Matched skills ({fit.matched_skills.length})
          </p>
          <SkillChips
            skills={fit.matched_skills}
            variant="matched"
            emptyText="No required skills were found in the resume yet."
          />
        </div>

        <div>
          <p className="mb-2 text-sm font-medium text-ink">
            Missing skills ({fit.missing_skills.length})
          </p>
          <SkillChips
            skills={fit.missing_skills}
            variant="missing"
            emptyText="Every skill mentioned in the job description shows up in this resume."
          />
        </div>

        {fit.extra_resume_skills.length > 0 && (
          <div>
            <p className="mb-2 text-sm font-medium text-ink">
              Other skills on the resume ({fit.extra_resume_skills.length})
            </p>
            <SkillChips skills={fit.extra_resume_skills} variant="extra" />
          </div>
        )}
      </div>
    </div>
  );
}
