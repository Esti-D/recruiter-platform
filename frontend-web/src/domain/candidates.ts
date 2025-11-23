// src/domain/Candidate.ts

export interface Candidate {
  candidateId: string;
  name: string;
  dni: string;
  role: string;
  location: string;
  status: string;
  notes: string;
  experience?: string;   // opcional
  strength?: string;     // opcional
  salaryRange?: string;  // opcional
  createdAt: string;
  updatedAt?: string;    // solo cuando se edita
}
