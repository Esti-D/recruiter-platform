// src/infrastructure/api/rolesApi.ts
import { apiConfig } from "../../config/api";
import { Role } from "../../domain/roles";

const BASE_URL = `${apiConfig.baseUrl}/roles`;

async function handleJsonOrThrow(res: Response, defaultMessage: string) {
  if (res.ok) return res.json();

  let extra = "";
  try { extra = (await res.text()) || ""; } catch {}

  throw new Error(`${defaultMessage} (HTTP ${res.status}) ${extra}`);
}

async function handleVoidOrThrow(res: Response, defaultMessage: string) {
  if (res.ok) return;

  let extra = "";
  try { extra = (await res.text()) || ""; } catch {}

  throw new Error(`${defaultMessage} (HTTP ${res.status}) ${extra}`);
}

export const rolesApi = {

  async getAll(params?: { q?: string }): Promise<Role[]> {
    const url =
      params?.q ? `${BASE_URL}?q=${encodeURIComponent(params.q)}` : BASE_URL;

    const res = await fetch(url, {
      headers: apiConfig.withAuthHeaders(),   // ✅ CAMBIO
    });

    return handleJsonOrThrow(res, "Error fetching roles");
  },

  async getById(roleId: string): Promise<Role> {
    const res = await fetch(`${BASE_URL}/${roleId}`, {
      headers: apiConfig.withAuthHeaders(),   // ✅ CAMBIO
    });

    return handleJsonOrThrow(res, "Error fetching role");
  },

  async create(role: Omit<Role, "roleId" | "createdAt">): Promise<Role> {
    const res = await fetch(BASE_URL, {
      method: "POST",
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),                                     // ✅ CAMBIO
      body: JSON.stringify(role),
    });

    return handleJsonOrThrow(res, "Error creating role");
  },

  async update(roleId: string, role: Partial<Role>): Promise<Role> {
    const res = await fetch(`${BASE_URL}/${roleId}`, {
      method: "PATCH",
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),                                     // ✅ CAMBIO
      body: JSON.stringify(role),
    });

    return handleJsonOrThrow(res, "Error updating role");
  },

  async delete(roleId: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/${roleId}`, {
      method: "DELETE",
      headers: apiConfig.withAuthHeaders(),   // ✅ CAMBIO
    });

    return handleVoidOrThrow(res, "Error deleting role");
  },

  async reassign(oldRoleId: string, newRoleId: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/${oldRoleId}/reassign`, {
      method: "POST",
      headers: apiConfig.withAuthHeaders({
        "Content-Type": "application/json",
      }),                                     // ❗ NECESARIO
      body: JSON.stringify({ newRoleId }),
    });

    return handleVoidOrThrow(res, "Error reassigning role");
  },
};
