// src/domain/Offer.ts

export interface Offer {
  offerId: string;
  companyName: string;
  contactPerson: string;
  role: string;
  modality: string;
  location: string;
  description: string;
  createdAt: string;
  updatedAt?: string; // opcional
  workflow?: "CREATED" | "REVIEWED";
}
