// src/ui/pages/ProcessesPage.tsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Process } from "../../domain/processes";
import { processesApi } from "../../infrastructure/api/processesApi";
import {
  Box,
  CircularProgress,
  Typography,
  Stack,
  Button
} from "@mui/material";
import { useTranslation } from "react-i18next";
import ProcessesTable from "../components/tables/ProcessesTable";

export default function ProcessesPage() {
  const { t } = useTranslation("common");
  const navigate = useNavigate();

  const [processes, setProcesses] = useState<Process[]>([]);
  const [loading, setLoading] = useState(true);

  const loadProcesses = () => {
    setLoading(true);
    processesApi
      .getAll()
      .then(setProcesses)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadProcesses();
  }, []);

  const handleOpenDetail = (process: Process) => {
    navigate(`/processes/${process.processId}`);
  };

  const handleCloseProcess = async (process: Process) => {
    const ok = window.confirm(
      t("processes.confirmClose", { id: process.processId })
    );
    if (!ok) return;

    try {
      await processesApi.update(process.processId, { status: "CLOSED" });
      loadProcesses();
    } catch (err) {
      console.error(err);
      // cuando tengamos backend real podemos meter un snackbar
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        mb={2}
      >
        <Typography variant="h5">{t("processes.title")}</Typography>
        <Button variant="outlined" onClick={loadProcesses}>
          {t("processes.reload", "Reload")}
        </Button>
      </Stack>

      <ProcessesTable
        processes={processes}
        onOpen={handleOpenDetail}
        onClose={handleCloseProcess}
      />
    </Box>
  );
}
