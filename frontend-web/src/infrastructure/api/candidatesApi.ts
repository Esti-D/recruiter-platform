// src/infrastructure/api/candidatesApi.ts
import { apiConfig } from "../../config/api";
import { Candidate } from "../../domain/candidates";

const BASE_URL = `${apiConfig.baseUrl}/candidates`;

async function handleJsonOrThrow(res: Response, defaultMessage: string) {
  if (res.ok) return res.json();

  let extra = "";
  try {
    extra = await res.text();
  } catch {}

  throw new Error(`${defaultMessage} (HTTP ${res.status}) ${extra}`);
}

async function handleVoidOrThrow(res: Response, defaultMessage: string) {
  if (res.ok) return;
  let extra = "";
  try {
    extra = await res.text();
  } catch {}
  throw new Error(`${defaultMessage} (HTTP ${res.status}) ${extra}`);
}

export const candidatesApi = {
  async getAll(params?: Record<string, string>): Promise<Candidate[]> {
    const url = new URL(BASE_URL);

    if (params) {
      Object.entries(params).forEach(([k, v]) => {
        if (v) url.searchParams.append(k, v);
      });
    }

    const res = await fetch(url, {
      headers: apiConfig.withAuthHeaders(),
    });
    return handleJsonOrThrow(res, "Error fetching candidates");
  },

  async getById(candidateId: string): Promise<Candidate> {
    const res = await fetch(`${BASE_URL}/${candidateId}`, {
      headers: apiConfig.withAuthHeaders(),
    });
    return handleJsonOrThrow(res, "Error fetching candidate");
  },

  async create(
    candidate: Omit<Candidate, "candidateId" | "createdAt" | "updatedAt">
  ): Promise<Candidate> {
    const res = await fetch(BASE_URL, {
      method: "POST",
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(candidate),
    });
    return handleJsonOrThrow(res, "Error creating candidate");
  },

  async update(
    candidateId: string,
    changes: Partial<Candidate>
  ): Promise<Candidate> {
    const res = await fetch(`${BASE_URL}/${candidateId}`, {
      method: "PATCH",
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(changes),
    });
    return handleJsonOrThrow(res, "Error updating candidate");
  },

  async delete(candidateId: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/${candidateId}`, {
      method: "DELETE",
      headers: apiConfig.withAuthHeaders(),
    });
    return handleVoidOrThrow(res, "Error deleting candidate");
  },
};
