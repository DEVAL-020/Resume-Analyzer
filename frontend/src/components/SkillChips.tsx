interface SkillChipsProps {
  skills: string[];
  variant: "matched" | "missing" | "extra";
  emptyText?: string;
}

const VARIANT_STYLES: Record<SkillChipsProps["variant"], string> = {
  matched: "bg-match-soft text-match border border-match/30",
  missing: "bg-gap-soft text-gap border border-gap/30",
  extra: "bg-paper-card text-ink-soft border border-paper-line",
};

export default function SkillChips({ skills, variant, emptyText }: SkillChipsProps) {
  if (skills.length === 0) {
    return emptyText ? <p className="text-sm text-ink-faint italic">{emptyText}</p> : null;
  }

  return (
    <div className="flex flex-wrap gap-2">
      {skills.map((skill) => (
        <span
          key={skill}
          className={`inline-block rounded-full px-3 py-1 text-sm font-medium capitalize transition-all duration-300 hover:-translate-y-0.5 hover:shadow-card ${VARIANT_STYLES[variant]}`}
        >
          {skill}
        </span>
      ))}
    </div>
  );
}
