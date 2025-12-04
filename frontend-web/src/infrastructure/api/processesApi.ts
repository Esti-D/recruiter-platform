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
  async getAll(): Promise<Process[]> {
    const res = await fetch(BASE_URL, {
      headers: apiConfig.withAuthHeaders(),
    });
    if (!res.ok) throw new Error("Error fetching processes");
    return res.json();
  },

  async getById(processId: string): Promise<Process> {
    const res = await fetch(`${BASE_URL}/${processId}`, {
      headers: apiConfig.withAuthHeaders(),
    });
    if (!res.ok) throw new Error("Error fetching process");
    return res.json();
  },

  async getByOfferId(offerId: string): Promise<Process | null> {
    const url = new URL(BASE_URL);
    url.searchParams.append("offerId", offerId);

    const res = await fetch(url, {
      headers: apiConfig.withAuthHeaders(),
    });

    if (res.status === 404) return null;
    if (!res.ok) throw new Error("Error fetching process by offerId");

    return res.json();
  },

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
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error("Error creating process from offer");
    return res.json();
  },

  async update(processId: string, changes: Partial<Process>): Promise<Process> {
    const res = await fetch(`${BASE_URL}/${processId}`, {
      method: "PATCH",
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(changes),
    });

    if (!res.ok) throw new Error("Error updating process");
    return res.json();
  },

  async close(processId: string): Promise<Process> {
    const res = await fetch(`${BASE_URL}/${processId}`, {
      method: "PATCH",
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({ status: "CLOSED" }),
    });

    if (!res.ok) throw new Error("Error closing process");
    return res.json();
  },

  async generateCandidates(
    processId: string,
    similarRoles: string[]
  ): Promise<GenerateCandidatesResponse> {
    const res = await fetch(`${BASE_URL}/${processId}/candidates:generate`, {
      method: "POST",
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({ similarRoles }),
    });

    if (!res.ok) throw new Error("Error generating candidates for process");
    return res.json();
  },
};
