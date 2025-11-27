// src/infrastructure/api/processesApi.ts
import { apiConfig } from "../../config/api";
import { Process } from "../../domain/processes";
import { Offer } from "../../domain/offers";

const BASE_URL = `${apiConfig.baseUrl}/processes`;

interface GenerateCandidatesResponse {
  processId: string;
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

  // Obtener proceso por oferta (si lo usas)
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

  // Crear proceso a partir de una oferta
  // Tu lambda espera { offerId, recruiter, notes }
  async createFromOffer(
    offer: Offer,
    recruiter: string,
    notes = ""
  ): Promise<Process> {
    const payload = {
      offerId: offer.offerId,
      recruiter,
      notes,
    };

    const res = await fetch(BASE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error("Error creating process from offer");
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
      body: JSON.stringify(changes),
    });

    if (!res.ok) {
      throw new Error("Error updating process");
    }
    return res.json();
  },

  // Cerrar proceso
  async close(processId: string): Promise<Process> {
    const res = await fetch(`${BASE_URL}/${processId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: "CLOSED" }),
    });

    if (!res.ok) {
      throw new Error("Error closing process");
    }
    return res.json();
  },

  // Generar candidatos (tu backend espera similarRoles)
  async generateCandidates(
    processId: string,
    similarRoles: string[]
  ): Promise<GenerateCandidatesResponse> {
    const res = await fetch(`${BASE_URL}/${processId}/candidates:generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ similarRoles }),
    });

    if (!res.ok) {
      throw new Error("Error generating candidates for process");
    }
    return res.json();
  },
};
