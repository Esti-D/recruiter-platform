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

export default function SettingsPage() {
  const { t } = useTranslation("common");
  const currentLang = i18n.language || "en";

  const handleChangeLang = (event: SelectChangeEvent<string>) => {
    const lang = event.target.value as string;
    i18n.changeLanguage(lang);
  };

  return (
    <Box>
      <Typography variant="h5" mb={3}>
        {t("nav.settings")}
      </Typography>

      <Stack spacing={2} maxWidth={300}>
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
      </Stack>
    </Box>
  );
}
