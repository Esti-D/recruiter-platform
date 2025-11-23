// src/infrastructure/api/rolesApi.ts
import { apiConfig } from "../../config/api";
import { Role } from "../../domain/roles";

const BASE_URL = `${apiConfig.baseUrl}/roles`;

async function handleJsonOrThrow(res: Response, defaultMessage: string) {
  if (res.ok) {
    return res.json();
  }
  let extra = "";
  try {
    const text = await res.text();
    extra = text ? ` - ${text}` : "";
  } catch {
    // ignoramos
  }
  throw new Error(`${defaultMessage} (HTTP ${res.status})${extra}`);
}

async function handleVoidOrThrow(res: Response, defaultMessage: string) {
  if (res.ok) return;
  let extra = "";
  try {
    const text = await res.text();
    extra = text ? ` - ${text}` : "";
  } catch {
    // ignoramos
  }
  throw new Error(`${defaultMessage} (HTTP ${res.status})${extra}`);
}

export const rolesApi = {
  // Listar roles (con filtro q opcional)
  async getAll(params?: { q?: string }): Promise<Role[]> {
    const url =
      params?.q != null && params.q !== ""
        ? `${BASE_URL}?q=${encodeURIComponent(params.q)}`
        : BASE_URL;

    const res = await fetch(url);
    return handleJsonOrThrow(res, "Error fetching roles");
  },

  // Obtener un rol por ID
  async getById(roleId: string): Promise<Role> {
    const res = await fetch(`${BASE_URL}/${roleId}`);
    return handleJsonOrThrow(res, "Error fetching role");
  },

  // Crear rol
  async create(role: Omit<Role, "roleId" | "createdAt">): Promise<Role> {
    const res = await fetch(BASE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(role)
    });

    return handleJsonOrThrow(res, "Error creating role");
  },

  // Actualizar rol
  async update(roleId: string, role: Partial<Role>): Promise<Role> {
    const res = await fetch(`${BASE_URL}/${roleId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(role)
    });

    return handleJsonOrThrow(res, "Error updating role");
  },

  // Borrar rol (solo si no está en uso)
  async delete(roleId: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/${roleId}`, {
      method: "DELETE"
    });

    return handleVoidOrThrow(res, "Error deleting role");
  },

  // Reasignar rol → necesario si el backend indica "role in use"
  async reassign(oldRoleId: string, newRoleId: string): Promise<void> {
    const res = await fetch(`${BASE_URL}/${oldRoleId}/reassign`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ newRoleId })
    });

    return handleVoidOrThrow(res, "Error reassigning role");
  }
};
