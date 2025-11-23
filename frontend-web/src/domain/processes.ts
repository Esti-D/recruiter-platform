// src/domain/processes.ts

export interface ProcessCandidate {
  candidateId: string;
  name: string;
  role: string;

  // Campos propios de la participación en este proceso
  experience?: string | null;
  strength?: string | null;
  salaryRange?: string | null;
  state?: string | null;
  notes?: string | null;
}

export type ProcessStatus = "OPEN" | "PAUSED" | "CLOSED";

export interface Process {
  processId: string;
  offerId: string;
  roleOffer: string;
  similarRoles: string[]; // nombres de roles similares
  recruiter: string | null;
  notes: string | null;
  status: ProcessStatus;
  createdAt: string;
  closedAt?: string | null;
  candidates: ProcessCandidate[];
}
