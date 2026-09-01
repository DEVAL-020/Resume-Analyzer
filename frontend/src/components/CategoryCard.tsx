import type { CategoryPrediction } from "../types";

function formatCategory(raw: string): string {
  return raw
    .toLowerCase()
    .split("-")
    .map((w) => w[0].toUpperCase() + w.slice(1))
    .join(" ");
}

export default function CategoryCard({ prediction }: { prediction: CategoryPrediction }) {
  const confidencePct = Math.round(prediction.confidence * 100);

  return (
    <div className="lift-on-hover rounded-2xl border border-paper-line bg-paper-card p-6 shadow-card hover:border-ink-faint/40 hover:shadow-card-hover">
      <h3 className="font-display text-lg font-semibold text-ink">Predicted category</h3>
      <p className="mt-3 font-display text-3xl font-semibold text-ink">
        {formatCategory(prediction.category)}
      </p>
      <p className="mt-1 text-sm text-ink-soft">{confidencePct}% model confidence</p>

      {prediction.top_categories.length > 1 && (
        <div className="mt-4 space-y-2">
          {prediction.top_categories.map((c) => (
            <div key={c.category} className="flex items-center gap-3">
              <span className="w-40 shrink-0 truncate text-sm text-ink-soft">
                {formatCategory(c.category)}
              </span>
              <div className="h-2 flex-1 rounded-full bg-paper">
                <div
                  className="h-2 rounded-full bg-highlighter-deep transition-[width] duration-700 ease-out"
                  style={{ width: `${Math.max(2, c.confidence * 100)}%` }}
                />
              </div>
              <span className="w-10 shrink-0 text-right text-xs text-ink-faint">
                {Math.round(c.confidence * 100)}%
              </span>
            </div>
          ))}
        </div>
      )}

      {prediction.explanation_terms.length > 0 && (
        <div className="mt-5 border-t border-paper-line pt-4">
          <p className="text-sm text-ink-soft">
            Words in the resume that drove this prediction:
          </p>
          <p className="mt-2 leading-8">
            {prediction.explanation_terms.map((term) => (
              <span key={term} className="highlight-mark mr-1 font-medium">
                {term}
              </span>
            ))}
          </p>
        </div>
      )}
    </div>
  );
}
