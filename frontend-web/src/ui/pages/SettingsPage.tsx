import { Box, Typography, FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import { useState } from "react";

const languages = [
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
  const [lang, setLang] = useState<string>("en");

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Settings
      </Typography>

      <FormControl sx={{ mt: 2, minWidth: 240 }}>
        <InputLabel id="language-select-label">Language</InputLabel>
        <Select
          labelId="language-select-label"
          label="Language"
          value={lang}
          onChange={(e) => setLang(e.target.value)}
        >
          {languages.map((l) => (
            <MenuItem key={l.code} value={l.code}>
              {l.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Typography variant="body2" sx={{ mt: 2, color: "text.secondary" }}>
        (Más adelante aquí conectaremos con i18next para que cambie el idioma real de la app.)
      </Typography>
    </Box>
  );
}
