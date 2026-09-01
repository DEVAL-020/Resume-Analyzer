import type { AnalyzeResponse, HealthResponse } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiRequestError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = "ApiRequestError";
  }
}

async function parseErrorDetail(res: Response): Promise<string> {
  try {
    const body = await res.json();
    if (typeof body?.detail === "string") return body.detail;
  } catch {

  }
  return `Request failed with status ${res.status}`;
}

export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new ApiRequestError(await parseErrorDetail(res), res.status);
  return res.json();
}

export async function analyzeResume(
  file: File,
  jobDescription: string
): Promise<AnalyzeResponse> {
  const formData = new FormData();
  formData.append("resume", file);
  if (jobDescription.trim().length > 0) {
    formData.append("job_description", jobDescription);
  }

  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new ApiRequestError(await parseErrorDetail(res), res.status);
  return res.json();
}
