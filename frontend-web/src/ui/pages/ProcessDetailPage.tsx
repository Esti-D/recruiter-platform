// src/ui/pages/ProcessDetailPage.tsx
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Process, ProcessCandidate, ProcessStatus } from "../../domain/processes";
import { processesApi } from "../../infrastructure/api/processesApi";
import { rolesApi } from "../../infrastructure/api/rolesApi";
import { Role } from "../../domain/roles";
import {
  Box,
  CircularProgress,
  Typography,
  Stack,
  Button,
  Chip,
  Divider,
  TextField,
  MenuItem,
  FormGroup,
  FormControlLabel,
  Checkbox
} from "@mui/material";
import { useTranslation } from "react-i18next";
import ProcessCandidatesTable from "../components/tables/ProcessCandidatesTable";

type ProcessForm = {
  recruiter: string;
  status: ProcessStatus;
  notes: string;
};

export default function ProcessDetailPage() {
  const { t } = useTranslation("common");
  const { processId } = useParams<{ processId: string }>();
  const navigate = useNavigate();

  const [process, setProcess] = useState<Process | null>(null);
  const [candidates, setCandidates] = useState<ProcessCandidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [savingProcess, setSavingProcess] = useState(false);
  const [savingCandidates, setSavingCandidates] = useState(false);

  const [roles, setRoles] = useState<Role[]>([]);
  const [selectedRoles, setSelectedRoles] = useState<string[]>([]); // nombres de roles similares

  const [form, setForm] = useState<ProcessForm>({
    recruiter: "",
    status: "OPEN",
    notes: ""
  });

  const loadProcess = () => {
    if (!processId) return;
    setLoading(true);

    processesApi
      .getById(processId)
      .then((p) => {
        setProcess(p);
        setCandidates(p.candidates ?? []);
        setForm({
          recruiter: p.recruiter ?? "",
          status: p.status,
          notes: p.notes ?? ""
        });
        setSelectedRoles(p.similarRoles ?? []);
      })
      .finally(() => setLoading(false));
  };

  const loadRoles = () => {
    rolesApi
      .getAll()
      .then((rs) => setRoles(rs))
      .catch((err) => console.error("Error loading roles", err));
  };

  useEffect(() => {
    loadProcess();
    loadRoles();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [processId]);

  const handleBack = () => {
    navigate("/processes");
  };

  const handleFormChange =
    (field: keyof ProcessForm) =>
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const value = event.target.value;
      setForm((prev) => ({ ...prev, [field]: value as any }));
    };

  const handleStatusChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value as ProcessStatus;
    setForm((prev) => ({ ...prev, status: value }));
  };

  const handleToggleRole = (roleName: string) => (
    _event: React.ChangeEvent<HTMLInputElement>,
    checked: boolean
  ) => {
    setSelectedRoles((prev) =>
      checked ? [...prev, roleName] : prev.filter((r) => r !== roleName)
    );
  };

  const handleSaveProcess = async () => {
    if (!processId) return;
    setSavingProcess(true);
    try {
      await processesApi.update(processId, {
        recruiter: form.recruiter || null,
        status: form.status,
        notes: form.notes || null
        // similarRoles se actualiza normalmente desde generateCandidates en backend
      });
      loadProcess();
    } catch (err) {
      console.error(err);
    } finally {
      setSavingProcess(false);
    }
  };

  const handleGenerateCandidates = async () => {
    if (!processId) return;
    try {
      await processesApi.generateCandidates(processId, selectedRoles);
      loadProcess();
    } catch (err) {
      console.error(err);
    }
  };

  const handleSaveCandidates = async () => {
    if (!processId) return;
    setSavingCandidates(true);
    try {
      await processesApi.update(processId, { candidates });
      loadProcess();
    } catch (err) {
      console.error(err);
    } finally {
      setSavingCandidates(false);
    }
  };

  if (loading || !process) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      {/* Top bar */}
      <Stack
        direction="row"
        alignItems="center"
        justifyContent="space-between"
        mb={2}
      >
        <Stack direction="row" spacing={2} alignItems="center">
          <Button variant="outlined" onClick={handleBack}>
            {t("processes.back")}
          </Button>

          <Typography variant="h5">
            {t("processes.detailTitle", { id: process.processId })}
          </Typography>

          <Chip
            label={process.status}
            color={
              process.status === "OPEN"
                ? "success"
                : process.status === "PAUSED"
                ? "warning"
                : "default"
            }
            size="small"
          />
        </Stack>

        <Button
          variant="contained"
          onClick={handleSaveProcess}
          disabled={savingProcess}
        >
          {t("processes.saveProcess")}
        </Button>
      </Stack>

      {/* Process info */}
      <Stack spacing={1} mb={2}>
        <Typography variant="body2">
          <strong>{t("processes.fields.processId")}:</strong> {process.processId}
        </Typography>
        <Typography variant="body2">
          <strong>{t("processes.fields.offerId")}:</strong> {process.offerId}
        </Typography>
        <Typography variant="body2">
          <strong>{t("processes.fields.roleOffer")}:</strong> {process.roleOffer}
        </Typography>

        <TextField
          label={t("processes.fields.recruiter")}
          value={form.recruiter}
          onChange={handleFormChange("recruiter")}
          size="small"
          sx={{ maxWidth: 300, mt: 1 }}
        />

        <TextField
          select
          label={t("processes.fields.status")}
          value={form.status}
          onChange={handleStatusChange}
          size="small"
          sx={{ maxWidth: 200, mt: 1 }}
        >
          <MenuItem value="OPEN">OPEN</MenuItem>
          <MenuItem value="PAUSED">PAUSED</MenuItem>
          <MenuItem value="CLOSED">CLOSED</MenuItem>
        </TextField>

        <TextField
          label={t("processes.fields.notes")}
          value={form.notes}
          onChange={handleFormChange("notes")}
          size="small"
          multiline
          minRows={2}
          sx={{ mt: 1 }}
        />
      </Stack>

      <Divider sx={{ my: 2 }} />

      {/* Similar roles */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 1 }}>
          {t("processes.similarRoles.title")}
        </Typography>

        <Stack direction="row" spacing={2} alignItems="flex-start">
          <FormGroup row>
            {roles.map((r) => (
              <FormControlLabel
                key={r.roleId}
                control={
                  <Checkbox
                    checked={selectedRoles.includes(r.name)}
                    onChange={handleToggleRole(r.name)}
                  />
                }
                label={r.name}
              />
            ))}
          </FormGroup>

          <Button
            variant="outlined"
            onClick={handleGenerateCandidates}
            disabled={process.status === "CLOSED"}
          >
            {t("processes.generateCandidates")}
          </Button>
        </Stack>
      </Box>

      <Divider sx={{ my: 2 }} />

      {/* Candidates in process */}
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        mb={1}
      >
        <Typography variant="h6">
          {t("processes.detailCandidatesTitle")}
        </Typography>

        <Button
          variant="contained"
          onClick={handleSaveCandidates}
          disabled={savingCandidates || process.status === "CLOSED"}
        >
          {t("processes.saveCandidates")}
        </Button>
      </Stack>

      <ProcessCandidatesTable
        candidates={candidates}
        onChange={setCandidates}
        disabled={process.status === "CLOSED"}
      />
    </Box>
  );
}
