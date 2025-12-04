// src/infrastructure/api/offersApi.ts
import { apiConfig } from "../../config/api";
import { Offer } from "../../domain/offers";

const BASE_URL = `${apiConfig.baseUrl}/offers`;

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

export const offersApi = {
  async getAll(params?: Record<string, string>): Promise<Offer[]> {
    const url = new URL(BASE_URL);
    if (params) {
      Object.entries(params).forEach(([k, v]) => {
        if (v) url.searchParams.append(k, v);
      });
    }

    const res = await fetch(url, {
      headers: apiConfig.withAuthHeaders(),
    });
    return handleJsonOrThrow(res, "Error fetching offers");
  },

  async getById(offerId: string): Promise<Offer> {
    const res = await fetch(`${BASE_URL}/${offerId}`, {
      headers: apiConfig.withAuthHeaders(),
    });
    return handleJsonOrThrow(res, "Error fetching offer");
  },

  async create(
    offer: Omit<Offer, "offerId" | "createdAt" | "updatedAt">
  ): Promise<Offer> {
    const res = await fetch(BASE_URL, {
      method: "POST",
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(offer),
    });
    return handleJsonOrThrow(res, "Error creating offer");
  },

  async update(offerId: string, changes: Partial<Offer>): Promise<Offer> {
    const res = await fetch(`${BASE_URL}/${offerId}`, {
      method: "PATCH",
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(changes),
    });
    return handleJsonOrThrow(res, "Error updating offer");
  },

  async delete(offerId: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/${offerId}`, {
      method: "DELETE",
      headers: apiConfig.withAuthHeaders(),
    });

    return handleVoidOrThrow(res, "Error deleting offer");
  },
};
