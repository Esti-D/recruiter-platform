// src/ui/pages/WorkflowPage.tsx
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import IconButton from "@mui/material/IconButton";
import Chip from "@mui/material/Chip";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";

import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { Candidate } from "../../domain/candidates";
import { Offer } from "../../domain/offers";
import { candidatesApi } from "../../infrastructure/api/candidatesApi";
import { offersApi } from "../../infrastructure/api/offersApi";

// 👇 truco para que TS deje de quejarse con Grid
const MuiGrid = Grid as any;

// Añadimos workflow opcional para evitar errores de tipo
type WorkflowCandidate = Candidate & { workflow?: string };
type WorkflowOffer = Offer & { workflow?: string };

export default function WorkflowPage() {
  const { t } = useTranslation("common");
  const [candidates, setCandidates] = useState<WorkflowCandidate[]>([]);
  const [offers, setOffers] = useState<WorkflowOffer[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [cList, oList] = await Promise.all([
        candidatesApi.getAll({ workflow: "CREATED" }),
        offersApi.getAll({ workflow: "CREATED" })
      ]);

      setCandidates(cList);
      setOffers(oList);
    } catch (e) {
      console.error("Error fetching workflow data:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const validateCandidate = async (id: string) => {
    try {
      await candidatesApi.update(id, { workflow: "REVIEWED" } as any);
      setCandidates((prev) => prev.filter((c) => c.candidateId !== id));
    } catch (e) {
      console.error("Error validating candidate", e);
    }
  };

  const validateOffer = async (id: string) => {
    try {
      await offersApi.update(id, { workflow: "REVIEWED" } as any);
      setOffers((prev) => prev.filter((o) => o.offerId !== id));
    } catch (e) {
      console.error("Error validating offer", e);
    }
  };

  return (
    <Box>
      <Stack direction="row" justifyContent="space-between" mb={3}>
        <Typography variant="h5" fontWeight={600}>
          {t("workflow.title", "Workflow de validación")}
        </Typography>
        {loading && (
          <Typography variant="body2" color="text.secondary">
            {t("workflow.loading", "Cargando pendientes…")}
          </Typography>
        )}
      </Stack>

      <MuiGrid container spacing={3}>
        {/* ---- CANDIDATOS ---- */}
        <MuiGrid item xs={12} md={6}>
          <Card variant="outlined">
            <CardHeader
              title={t("workflow.candidates", "Candidatos pendientes")}
              subheader={t(
                "workflow.candidates_sub",
                "Creados por candidatos, a la espera de revisión"
              )}
            />
            <CardContent>
              {candidates.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  {t("workflow.no_candidates", "No hay candidatos pendientes.")}
                </Typography>
              ) : (
                <List dense>
                  {candidates.map((c) => (
                    <ListItem
                      key={c.candidateId}
                      secondaryAction={
                        <IconButton
                          edge="end"
                          onClick={() => validateCandidate(c.candidateId)}
                        >
                          <CheckCircleIcon />
                        </IconButton>
                      }
                    >
                      <ListItemIcon>
                        <WarningAmberIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Stack direction="row" spacing={1} alignItems="center">
                            <Typography>{c.name}</Typography>
                            {c.role && (
                              <Chip size="small" label={c.role} variant="outlined" />
                            )}
                          </Stack>
                        }
                        secondary={
                          c.location ??
                          t("workflow.created_by_candidate", "Alta de candidato")
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </MuiGrid>

        {/* ---- OFERTAS ---- */}
        <MuiGrid item xs={12} md={6}>
          <Card variant="outlined">
            <CardHeader
              title={t("workflow.offers", "Ofertas pendientes")}
              subheader={t(
                "workflow.offers_sub",
                "Creadas por empresas, a la espera de revisión"
              )}
            />
            <CardContent>
              {offers.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  {t("workflow.no_offers", "No hay ofertas pendientes.")}
                </Typography>
              ) : (
                <List dense>
                  {offers.map((o) => (
                    <ListItem
                      key={o.offerId}
                      secondaryAction={
                        <IconButton edge="end" onClick={() => validateOffer(o.offerId)}>
                          <CheckCircleIcon />
                        </IconButton>
                      }
                    >
                      <ListItemIcon>
                        <WarningAmberIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Stack direction="row" spacing={1} alignItems="center">
                            <Typography>{o.companyName}</Typography>
                            {o.role && (
                              <Chip size="small" label={o.role} variant="outlined" />
                            )}
                          </Stack>
                        }
                        secondary={
                          o.location ??
                          t("workflow.created_by_company", "Alta de oferta")
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </MuiGrid>
      </MuiGrid>
    </Box>
  );
}
