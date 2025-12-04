// src/router/index.tsx
import { Routes, Route, Navigate } from "react-router-dom";

import OfferPage from "../ui/pages/OfferPage";
import CandidatesPage from "../ui/pages/CandidatesPage";
import RolesPage from "../ui/pages/RolesPage";
import SettingsPage from "../ui/pages/SettingsPage";
import ProcessesPage from "../ui/pages/ProcessesPage";
import ProcessDetailPage from "../ui/pages/ProcessDetailPage";
import WorkflowPage from "../ui/pages/WorkflowPage";

import ProtectedRoute from "./ProtectedRoute";

export default function AppRouter() {
  return (
    <Routes>
      {/* HOME → redirige a ofertas */}
      <Route path="/" element={<Navigate to="/offers" replace />} />

      {/* OFFERS → company, recruiter, admin */}
      <Route
        path="/offers"
        element={
          <ProtectedRoute allowed={["company", "recruiter", "admin"]}>
            <OfferPage />
          </ProtectedRoute>
        }
      />

      {/* CANDIDATES → candidate, recruiter, admin */}
      <Route
        path="/candidates"
        element={
          <ProtectedRoute allowed={["candidate", "recruiter", "admin"]}>
            <CandidatesPage />
          </ProtectedRoute>
        }
      />

      {/* ROLES → solo recruiter y admin */}
      <Route
        path="/roles"
        element={
          <ProtectedRoute allowed={["recruiter", "admin"]}>
            <RolesPage />
          </ProtectedRoute>
        }
      />

      {/* WORKFLOW → solo recruiter y admin */}
      <Route
        path="/workflow"
        element={
          <ProtectedRoute allowed={["recruiter", "admin"]}>
            <WorkflowPage />
          </ProtectedRoute>
        }
      />

      {/* SETTINGS → todos */}
      <Route path="/settings" element={<SettingsPage />} />

      {/* PROCESSES → recruiter y admin */}
      <Route
        path="/processes"
        element={
          <ProtectedRoute allowed={["recruiter", "admin"]}>
            <ProcessesPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/processes/:processId"
        element={
          <ProtectedRoute allowed={["recruiter", "admin"]}>
            <ProcessDetailPage />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
