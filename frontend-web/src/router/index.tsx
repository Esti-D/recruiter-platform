// src/router/index.tsx
import { Routes, Route, Navigate } from "react-router-dom";
import OfferPage from "../ui/pages/OfferPage";
import CandidatesPage from "../ui/pages/CandidatesPage";
import RolesPage from "../ui/pages/RolesPage";
import SettingsPage from "../ui/pages/SettingsPage";
import ProcessesPage from "../ui/pages/ProcessesPage";
import ProcessDetailPage from "../ui/pages/ProcessDetailPage";

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/offers" replace />} />

      <Route path="/offers" element={<OfferPage />} />
      {/* De momento quitamos esta ruta porque OfferCandidatesPage no existe */}
      {/* <Route path="/offers/:offerId/candidates" element={<OfferCandidatesPage />} /> */}

      <Route path="/candidates" element={<CandidatesPage />} />
      <Route path="/roles" element={<RolesPage />} />
      <Route path="/settings" element={<SettingsPage />} />

      {/* Processes */}
      <Route path="/processes" element={<ProcessesPage />} />
      <Route path="/processes/:processId" element={<ProcessDetailPage />} />
    </Routes>
  );
}
