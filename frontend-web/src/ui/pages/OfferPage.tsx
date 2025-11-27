// src/ui/pages/OfferPage.tsx
import { useEffect, useState } from "react";
import { Offer } from "../../domain/offers";
import { offersApi } from "../../infrastructure/api/offersApi";
import { rolesApi } from "../../infrastructure/api/rolesApi";
import { processesApi } from "../../infrastructure/api/processesApi";

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
import OffersTable from "../components/tables/OffersTable";
import { useTranslation } from "react-i18next";

type OfferForm = Omit<Offer, "offerId" | "createdAt" | "updatedAt">;

const emptyForm: OfferForm = {
  companyName: "",
  contactPerson: "",
  role: "",
  modality: "",
  location: "",
  description: ""
};

export default function OfferPage() {
  const { t } = useTranslation("common");

  const [offers, setOffers] = useState<Offer[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingOffer, setEditingOffer] = useState<Offer | null>(null);
  const [form, setForm] = useState<OfferForm>(emptyForm);

  const loadOffers = () => {
    setLoading(true);
    offersApi
      .getAll()
      .then(setOffers)
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
    loadOffers();
    loadRoles();
  }, []);

  const handleOpenCreate = () => {
    setEditingOffer(null);
    setForm(emptyForm);
    setDialogOpen(true);
  };

  const handleOpenEdit = (offer: Offer) => {
    setEditingOffer(offer);
    const { offerId, createdAt, updatedAt, ...rest } = offer;
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
    (field: keyof OfferForm) =>
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setForm((prev) => ({ ...prev, [field]: event.target.value }));
    };

  const handleSave = async () => {
    setSaving(true);
    try {
      if (editingOffer) {
        // EDITAR OFERTA EXISTENTE
        await offersApi.update(editingOffer.offerId, form);
      } else {
        // CREAR OFERTA NUEVA
        const createdOffer = await offersApi.create(form);

        // 🔹 CREAR AUTOMÁTICAMENTE EL PROCESO ASOCIADO
        // De momento ponemos el recruiter fijo "Esti"
        try {
          await processesApi.createFromOffer(createdOffer, "Esti");
        } catch (err) {
          console.error("Error creating process from offer", err);
          // Para demo: no rompemos el flujo si falla crear el proceso
        }
      }

      setDialogOpen(false);
      loadOffers();
    } catch (err) {
      console.error(err);
      window.alert("Error saving offer");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (offer: Offer) => {
    const ok = window.confirm(
      t("offers.confirmDelete", {
        role: offer.role,
        company: offer.companyName
      })
    );
    if (!ok) return;

    try {
      await offersApi.delete(offer.offerId);
      loadOffers();
    } catch (err) {
      console.error(err);
      window.alert("Error deleting offer");
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
        <Typography variant="h5">{t("offers.title")}</Typography>
        <Button variant="contained" onClick={handleOpenCreate}>
          {t("offers.new")}
        </Button>
      </Stack>

      <OffersTable
        offers={offers}
        onEdit={handleOpenEdit}
        onDelete={handleDelete}
      />

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingOffer ? t("offers.edit") : t("offers.new")}
        </DialogTitle>
        <DialogContent dividers>
          <Stack spacing={2} mt={1}>
            <TextField
              label={t("offers.fields.companyName")}
              value={form.companyName}
              onChange={handleChange("companyName")}
              fullWidth
              required
            />
            <TextField
              label={t("offers.fields.contactPerson")}
              value={form.contactPerson}
              onChange={handleChange("contactPerson")}
              fullWidth
            />

            <TextField
              label={t("offers.fields.role")}
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
              label={t("offers.fields.modality")}
              value={form.modality}
              onChange={handleChange("modality")}
              fullWidth
            />
            <TextField
              label={t("offers.fields.location")}
              value={form.location}
              onChange={handleChange("location")}
              fullWidth
            />
            <TextField
              label={t("offers.fields.description")}
              value={form.description}
              onChange={handleChange("description")}
              fullWidth
              multiline
              minRows={2}
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} disabled={saving}>
            {t("offers.cancel")}
          </Button>
          <Button onClick={handleSave} variant="contained" disabled={saving}>
            {editingOffer ? t("offers.saveChanges") : t("offers.create")}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
