// src/infrastructure/api/processesApi.ts
import { apiConfig } from "../../config/api";
import { Process } from "../../domain/processes";

const BASE_URL = `${apiConfig.baseUrl}/processes`;

interface GenerateCandidatesResponse {
  count: number;
}

export const processesApi = {
  // Lista todos los procesos
  async getAll(): Promise<Process[]> {
    const res = await fetch(BASE_URL);
    if (!res.ok) {
      throw new Error("Error fetching processes");
    }
    return res.json();
  },

  // Obtener un proceso por ID
  async getById(processId: string): Promise<Process> {
    const res = await fetch(`${BASE_URL}/${processId}`);
    if (!res.ok) {
      throw new Error("Error fetching process");
    }
    return res.json();
  },

  // (Opcional) Obtener proceso por oferta, si lo necesitas
  async getByOfferId(offerId: string): Promise<Process | null> {
    const url = new URL(BASE_URL);
    url.searchParams.append("offerId", offerId);

    const res = await fetch(url);
    if (res.status === 404) {
      return null;
    }
    if (!res.ok) {
      throw new Error("Error fetching process by offerId");
    }
    return res.json();
  },

  // Actualizar proceso (parcial)
  async update(
    processId: string,
    changes: Partial<Process>
  ): Promise<Process> {
    const res = await fetch(`${BASE_URL}/${processId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(changes)
    });

    if (!res.ok) {
      throw new Error("Error updating process");
    }
    return res.json();
  },

  // Eliminar proceso
  async delete(processId: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/${processId}`, {
      method: "DELETE"
    });
    if (!res.ok) {
      throw new Error("Error deleting process");
    }
  },

  // Generar lista de candidatos para el proceso
  // Equivalente a generate_candidates(processId, selected_roles)
  async generateCandidates(
    processId: string,
    roles: string[]
  ): Promise<GenerateCandidatesResponse> {
    const res = await fetch(`${BASE_URL}/${processId}/generate-candidates`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ roles })
    });

    if (!res.ok) {
      throw new Error("Error generating candidates for process");
    }
    return res.json();
  }
};
