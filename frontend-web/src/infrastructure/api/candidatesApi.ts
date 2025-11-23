import { apiConfig } from "../../config/api";
import { Candidate } from "../../domain/candidates";

const BASE_URL = `${apiConfig.baseUrl}/candidates`;

export const candidatesApi = {
  // Obtener lista de candidatos con filtros opcionales
  async getAll(params?: Record<string, string>): Promise<Candidate[]> {
    const url = new URL(BASE_URL);

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value) url.searchParams.append(key, value);
      });
    }

    const res = await fetch(url);
    if (!res.ok) throw new Error("Error fetching candidates");
    return res.json();
  },

  // Obtener candidato por ID
  async getById(candidateId: string): Promise<Candidate> {
    const res = await fetch(`${BASE_URL}/${candidateId}`);
    if (!res.ok) throw new Error("Error fetching candidate");
    return res.json();
  },

  // Crear candidato
  async create(
    candidate: Omit<Candidate, "candidateId" | "createdAt" | "updatedAt">
  ): Promise<Candidate> {
    const res = await fetch(BASE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(candidate)
    });

    if (!res.ok) throw new Error("Error creating candidate");
    return res.json();
  },

  // Actualizar candidato (PATCH parcial)
  async update(
    candidateId: string,
    candidate: Partial<Candidate>
  ): Promise<Candidate> {
    const res = await fetch(`${BASE_URL}/${candidateId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(candidate)
    });

    if (!res.ok) throw new Error("Error updating candidate");
    return res.json();
  },

  // Borrar candidato
  async delete(candidateId: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/${candidateId}`, {
      method: "DELETE"
    });

    if (!res.ok) throw new Error("Error deleting candidate");
  }
};
