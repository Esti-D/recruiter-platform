// src/config/api.ts
import { cognitoAuth } from "./cognito";
import { roleStore } from "./role";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export const apiConfig = {
  baseUrl: API_BASE_URL,

  withAuthHeaders(extra?: HeadersInit): HeadersInit {
    const headers: Record<string, string> = {};

    // cabeceras extra que pase cada API (Content-Type, etc.)
    if (extra) {
      const h = new Headers(extra);
      h.forEach((v, k) => {
        headers[k] = v;
      });
    }

    const token = cognitoAuth.getIdToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const role = roleStore.getRole();
    if (role) {
      headers["X-Role"] = role;
    }

    // opcional, fijo para ahora
    headers["X-User-Id"] = "frontend-demo";

    return headers;
  },
};
