// src/config/cognito.ts
import { roleStore } from "./role";

const COGNITO_DOMAIN = import.meta.env.VITE_COGNITO_DOMAIN;
const COGNITO_CLIENT_ID = import.meta.env.VITE_COGNITO_CLIENT_ID;
const COGNITO_REDIRECT_URI = import.meta.env.VITE_COGNITO_REDIRECT_URI;
const COGNITO_LOGOUT_URI = import.meta.env.VITE_COGNITO_LOGOUT_URI;

const TOKEN_KEY = "cognito_id_token";

export const cognitoAuth = {
  getIdToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  setIdToken(token: string) {
    localStorage.setItem(TOKEN_KEY, token);
  },

  clearToken() {
    localStorage.removeItem(TOKEN_KEY);
  },

  login() {
    console.log("Cognito login", {
      COGNITO_DOMAIN,
      COGNITO_CLIENT_ID,
      COGNITO_REDIRECT_URI,
    });

    if (!COGNITO_DOMAIN || !COGNITO_CLIENT_ID || !COGNITO_REDIRECT_URI) {
      alert("Faltan variables de entorno de Cognito");
      return;
    }

    const url = new URL(`https://${COGNITO_DOMAIN}/oauth2/authorize`);
    url.searchParams.set("response_type", "token");
    url.searchParams.set("client_id", COGNITO_CLIENT_ID);
    url.searchParams.set("redirect_uri", COGNITO_REDIRECT_URI);
    url.searchParams.set("scope", "openid email profile");

    window.location.href = url.toString();
  },

  logout() {
    this.clearToken();

    if (!COGNITO_DOMAIN || !COGNITO_CLIENT_ID || !COGNITO_LOGOUT_URI) {
      window.location.href = "/";
      return;
    }

    const url = new URL(`https://${COGNITO_DOMAIN}/logout`);
    url.searchParams.set("client_id", COGNITO_CLIENT_ID);
    url.searchParams.set("logout_uri", COGNITO_LOGOUT_URI);

    window.location.href = url.toString();
  },

  handleRedirectCallback() {
    const hash = window.location.hash || "";
    if (!hash.startsWith("#")) return;

    const params = new URLSearchParams(hash.substring(1));
    const idToken = params.get("id_token");

    if (idToken) {
      this.setIdToken(idToken);
      
      try {
        const payload = JSON.parse(atob(idToken.split(".")[1]));
        const role = payload["custom:role"] || payload["role"];
        if (role) {
          roleStore.setRole(role as any);
        }
      } catch (e) {
        console.error("Error decoding token", e);
      }
          
      // limpiar el hash
      window.history.replaceState(null, "", window.location.pathname);
    }
  },
};
