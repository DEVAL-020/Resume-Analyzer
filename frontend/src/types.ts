export interface CategoryScore {
  category: string;
  confidence: number;
}

export interface CategoryPrediction {
  category: string;
  confidence: number;
  top_categories: CategoryScore[];
  explanation_terms: string[];
  model_used: string;
}

export interface JobFit {
  fit_score: number;
  text_similarity_pct: number;
  required_skills: string[];
  matched_skills: string[];
  missing_skills: string[];
  extra_resume_skills: string[];
  skill_coverage_pct: number;
}

export interface AnalyzeResponse {
  filename: string;
  word_count: number;
  category_prediction: CategoryPrediction;
  job_fit: JobFit | null;
}

export interface HealthResponse {
  status: string;
  model_ready: boolean;
  categories: string[];
}

export interface ApiError {
  detail: string;
}
