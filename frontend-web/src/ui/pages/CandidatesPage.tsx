import { useEffect, useState } from "react";
import { Candidate } from "../../domain/candidates";
import { candidatesApi } from "../../infrastructure/api/candidatesApi";
import { rolesApi } from "../../infrastructure/api/rolesApi";
import { Role } from "../../domain/roles";
import {
  Box,
  CircularProgress,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Stack,
  MenuItem
} from "@mui/material";
import CandidatesTable from "../components/tables/CandidatesTable";
import { useTranslation } from "react-i18next";

type CandidateForm = Omit<Candidate, "candidateId" | "createdAt" | "updatedAt">;

const emptyForm: CandidateForm = {
  name: "",
  dni: "",
  role: "",
  location: "",
  status: "",
  notes: "",
  experience: "",
  strength: "",
  salaryRange: ""
};

export default function CandidatesPage() {
  const { t } = useTranslation("common");

  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingCandidate, setEditingCandidate] = useState<Candidate | null>(null);
  const [form, setForm] = useState<CandidateForm>(emptyForm);

  const loadCandidates = () => {
    setLoading(true);
    candidatesApi
      .getAll()
      .then(setCandidates)
      .finally(() => setLoading(false));
  };

  const loadRoles = () => {
    rolesApi
      .getAll()
      .then(setRoles)
      .catch((err) => {
        console.error("Error loading roles", err);
      });
  };

  useEffect(() => {
    loadCandidates();
    loadRoles();
  }, []);

  const handleOpenCreate = () => {
    setEditingCandidate(null);
    setForm(emptyForm);
    setDialogOpen(true);
  };

  const handleOpenEdit = (candidate: Candidate) => {
    setEditingCandidate(candidate);
    const { candidateId, createdAt, updatedAt, ...rest } = candidate;
    setForm({
      ...emptyForm,
      ...rest
    });
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    if (saving) return;
    setDialogOpen(false);
  };

  const handleChange =
    (field: keyof CandidateForm) =>
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setForm((prev) => ({ ...prev, [field]: event.target.value }));
    };

  const handleSave = async () => {
    setSaving(true);
    try {
      if (editingCandidate) {
        await candidatesApi.update(editingCandidate.candidateId, form);
      } else {
        await candidatesApi.create(form);
      }
      setDialogOpen(false);
      loadCandidates();
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (candidate: Candidate) => {
    const ok = window.confirm(
      t("candidates.confirmDelete", { name: candidate.name })
    );
    if (!ok) return;
    try {
      await candidatesApi.delete(candidate.candidateId);
      loadCandidates();
    } catch (err) {
      console.error(err);
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
        <Typography variant="h5">{t("candidates.title")}</Typography>
        <Button variant="contained" onClick={handleOpenCreate}>
          {t("candidates.new")}
        </Button>
      </Stack>

      <CandidatesTable
        candidates={candidates}
        onEdit={handleOpenEdit}
        onDelete={handleDelete}
      />

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingCandidate ? t("candidates.edit") : t("candidates.new")}
        </DialogTitle>
        <DialogContent dividers>
          <Stack spacing={2} mt={1}>
            <TextField
              label={t("candidates.fields.name")}
              value={form.name}
              onChange={handleChange("name")}
              fullWidth
              required
            />
            <TextField
              label={t("candidates.fields.dni")}
              value={form.dni}
              onChange={handleChange("dni")}
              fullWidth
            />

            <TextField
              label={t("candidates.fields.role")}
              value={form.role}
              onChange={handleChange("role")}
              fullWidth
              select
            >
              {roles.map((role) => (
                <MenuItem key={role.roleId} value={role.name}>
                  {role.name}
                </MenuItem>
              ))}
            </TextField>

            <TextField
              label={t("candidates.fields.location")}
              value={form.location}
              onChange={handleChange("location")}
              fullWidth
            />
            <TextField
              label={t("candidates.fields.status")}
              value={form.status}
              onChange={handleChange("status")}
              fullWidth
            />
            <TextField
              label={t("candidates.fields.experience")}
              value={form.experience}
              onChange={handleChange("experience")}
              fullWidth
            />
            <TextField
              label={t("candidates.fields.strength")}
              value={form.strength}
              onChange={handleChange("strength")}
              fullWidth
            />
            <TextField
              label={t("candidates.fields.salaryRange")}
              value={form.salaryRange}
              onChange={handleChange("salaryRange")}
              fullWidth
            />
            <TextField
              label={t("candidates.fields.notes")}
              value={form.notes}
              onChange={handleChange("notes")}
              fullWidth
              multiline
              minRows={2}
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} disabled={saving}>
            {t("candidates.cancel")}
          </Button>
          <Button onClick={handleSave} variant="contained" disabled={saving}>
            {editingCandidate ? t("candidates.saveChanges") : t("candidates.create")}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

