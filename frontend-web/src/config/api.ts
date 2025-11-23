// src/config/api.ts

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "http://localhost:8000"; // cambia esto si tu backend usa otro puerto

export const apiConfig = {
  baseUrl: API_BASE_URL
};
