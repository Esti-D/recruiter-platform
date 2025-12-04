// src/config/role.ts
import { decodeJwt } from "../utils/jwt";
import { cognitoAuth } from "./cognito";

export const roleStore = {
  getRole() {
    const token = cognitoAuth.getIdToken();
    if (!token) return "recruiter";

    const payload = decodeJwt(token);
    return payload?.["custom:role"] ?? "recruiter";
  },

  getUserId() {
    const token = cognitoAuth.getIdToken();
    if (!token) return "user-recruiter";

    const payload = decodeJwt(token);
    return payload?.["custom:userId"] ?? "user-recruiter";
  },

  // se queda por compatibilidad, pero ya no lo usamos
  setRole(_role: string) {}
};

