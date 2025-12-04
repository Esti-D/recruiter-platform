// src/ui/pages/SettingsPage.tsx
import {
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack
} from "@mui/material";
import type { SelectChangeEvent } from "@mui/material/Select";
import { useTranslation } from "react-i18next";
import i18n from "../../i18n";
import { roleStore } from "../../config/role";
import { Button } from "@mui/material";
import { cognitoAuth } from "../../config/cognito";


const LANGS = [
  { code: "en", label: "English" },
  { code: "es", label: "Español" },
  { code: "eu", label: "Euskara" },
  { code: "ca", label: "Català" },
  { code: "fr", label: "Français" },
  { code: "de", label: "Deutsch" },
  { code: "it", label: "Italiano" },
  { code: "ga", label: "Gaeilge" },
  { code: "rm", label: "Rumantsch" }
];

// NUEVO — roles de usuario
const ROLES = [
  { code: "recruiter", label: "Recruiter" },
  { code: "candidate", label: "Candidate" },
  { code: "company", label: "Company" },
  { code: "admin", label: "Admin" }
];

export default function SettingsPage() {
  const { t } = useTranslation("common");

  const currentLang = i18n.language || "en";
  const currentRole = roleStore.getRole();

  const handleChangeLang = (event: SelectChangeEvent<string>) => {
    const lang = event.target.value as string;
    i18n.changeLanguage(lang);
  };

  const handleChangeRole = (event: SelectChangeEvent<string>) => {
    const role = event.target.value as string;
    roleStore.setRole(role as any);
  };

  return (
    <Box>
      <Typography variant="h5" mb={3}>
        {t("nav.settings")}
      </Typography>

      <Stack spacing={3} maxWidth={300}>

        {/* Selector de idioma */}
        <FormControl fullWidth size="small">
          <InputLabel id="lang-select-label">Idioma / Language</InputLabel>
          <Select
            labelId="lang-select-label"
            label="Idioma / Language"
            value={currentLang}
            onChange={handleChangeLang}
          >
            {LANGS.map((l) => (
              <MenuItem key={l.code} value={l.code}>
                {l.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* Selector de rol */}
        <FormControl fullWidth size="small">
          <InputLabel id="role-select-label">User role</InputLabel>
          <Select
            labelId="role-select-label"
            label="User role"
            value={currentRole}
            onChange={handleChangeRole}
          >
            {ROLES.map((r) => (
              <MenuItem key={r.code} value={r.code}>
                {r.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button variant="outlined" onClick={() => cognitoAuth.login()}>
          Login Cognito
        </Button>
        <Button variant="text" color="error" onClick={() => cognitoAuth.logout()}>
          Logout
        </Button>

      </Stack>
    </Box>
  );
}
