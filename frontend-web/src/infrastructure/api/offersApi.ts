// src/infrastructure/api/offersApi.ts
import { apiConfig } from "../../config/api";
import { Offer } from "../../domain/offers";

const BASE_URL = `${apiConfig.baseUrl}/offers`;

export const offersApi = {
  async getAll(params?: Record<string, string>): Promise<Offer[]> {
    const url = new URL(BASE_URL);

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value) url.searchParams.append(key, value);
      });
    }

    const res = await fetch(url);
    if (!res.ok) throw new Error("Error fetching offers");
    return res.json();
  },

  async getById(offerId: string): Promise<Offer> {
    const res = await fetch(`${BASE_URL}/${offerId}`);
    if (!res.ok) throw new Error("Error fetching offer");
    return res.json();
  },

  async create(
    offer: Omit<Offer, "offerId" | "createdAt" | "updatedAt">
  ): Promise<Offer> {
    const res = await fetch(BASE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(offer)
    });

    if (!res.ok) throw new Error("Error creating offer");
    return res.json();
  },

  async update(
    offerId: string,
    offer: Partial<Offer>
  ): Promise<Offer> {
    const res = await fetch(`${BASE_URL}/${offerId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(offer)
    });

    if (!res.ok) throw new Error("Error updating offer");
    return res.json();
  },

  async delete(offerId: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/${offerId}`, {
      method: "DELETE"
    });

    if (!res.ok) throw new Error("Error deleting offer");
  }
};

