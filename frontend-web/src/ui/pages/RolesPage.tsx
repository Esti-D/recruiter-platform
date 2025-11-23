// src/ui/pages/RolesPage.tsx
import { useEffect, useState } from "react";
import { Role } from "../../domain/roles";
import { rolesApi } from "../../infrastructure/api/rolesApi";
import {
  Box,
  CircularProgress,
  Typography,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Stack,
  MenuItem
} from "@mui/material";
import { useTranslation } from "react-i18next";
import RolesTable from "../components/tables/RolesTable";

type RoleForm = Omit<Role, "roleId" | "createdAt">;

const emptyForm: RoleForm = {
  name: ""
};

export default function RolesPage() {
  const { t } = useTranslation("common");

  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);

  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingRole, setEditingRole] = useState<Role | null>(null);
  const [form, setForm] = useState<RoleForm>(emptyForm);

  const [reassignDialog, setReassignDialog] = useState(false);
  const [roleToDelete, setRoleToDelete] = useState<Role | null>(null);
  const [replacementRole, setReplacementRole] = useState<string>("");

  const loadRoles = () => {
    setLoading(true);
    rolesApi
      .getAll()
      .then(setRoles)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadRoles();
  }, []);

  const handleOpenCreate = () => {
    setEditingRole(null);
    setForm(emptyForm);
    setDialogOpen(true);
  };

  const handleOpenEdit = (role: Role) => {
    setEditingRole(role);
    setForm({ name: role.name });
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
  };

  const handleChange =
    (field: keyof RoleForm) =>
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setForm((prev) => ({ ...prev, [field]: event.target.value }));
    };

  const handleSave = async () => {
    try {
      if (editingRole) {
        await rolesApi.update(editingRole.roleId, form);
      } else {
        await rolesApi.create(form);
      }
      setDialogOpen(false);
      loadRoles();
    } catch (err) {
      console.error(err);
      const message =
        err instanceof Error ? err.message : t("roles.errorSaving");
      // De momento algo sencillo, luego ya pondremos Snackbar si quieres
      window.alert(message);
    }
  };

  const handleDelete = async (role: Role) => {
    try {
      await rolesApi.delete(role.roleId);
      loadRoles();
    } catch (err) {
      // rol en uso → abrir diálogo de reasignación
      console.warn("Role in use, must reassign");
      setRoleToDelete(role);
      setReplacementRole("");
      setReassignDialog(true);
    }
  };

  const handleReassign = async () => {
    if (!roleToDelete || !replacementRole) return;

    try {
      await rolesApi.reassign(roleToDelete.roleId, replacementRole);
      setReassignDialog(false);
      loadRoles();
    } catch (err) {
      console.error("Error reassigning role", err);
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
        <Typography variant="h5">{t("roles.title")}</Typography>
        <Button variant="contained" onClick={handleOpenCreate}>
          {t("roles.new")}
        </Button>
      </Stack>

      <RolesTable
        roles={roles}
        onEdit={handleOpenEdit}
        onDelete={handleDelete}
      />

      {/* Create / Edit dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="xs" fullWidth>
        <DialogTitle>
          {editingRole ? t("roles.edit") : t("roles.new")}
        </DialogTitle>

        <DialogContent dividers>
          <Stack spacing={2}>
            <TextField
              label={t("roles.fields.name")}
              value={form.name}
              onChange={handleChange("name")}
              fullWidth
            />
          </Stack>
        </DialogContent>

        <DialogActions>
          <Button onClick={handleCloseDialog}>{t("roles.cancel")}</Button>
          <Button onClick={handleSave} variant="contained">
            {editingRole ? t("roles.saveChanges") : t("roles.create")}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Reassign dialog */}
      <Dialog open={reassignDialog} onClose={() => setReassignDialog(false)} maxWidth="xs" fullWidth>
        <DialogTitle>{t("roles.reassignTitle")}</DialogTitle>

        <DialogContent dividers>
          <Typography variant="body2" sx={{ mb: 2 }}>
            {t("roles.reassignText", { name: roleToDelete?.name })}
          </Typography>

          <TextField
            select
            fullWidth
            label={t("roles.fields.replacement")}
            value={replacementRole}
            onChange={(e) => setReplacementRole(e.target.value)}
          >
            {roles
              .filter((r) => r.roleId !== roleToDelete?.roleId)
              .map((r) => (
                <MenuItem key={r.roleId} value={r.roleId}>
                  {r.name}
                </MenuItem>
              ))}
          </TextField>
        </DialogContent>

        <DialogActions>
          <Button onClick={() => setReassignDialog(false)}>
            {t("roles.cancel")}
          </Button>
          <Button
            variant="contained"
            disabled={!replacementRole}
            onClick={handleReassign}
          >
            {t("roles.reassign")}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
