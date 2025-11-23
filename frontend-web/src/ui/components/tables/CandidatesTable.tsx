// src/ui/components/tables/CandidatesTable.tsx
import { Candidate } from "../../../domain/candidates";
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
  IconButton
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { useTranslation } from "react-i18next";

interface Props {
  candidates: Candidate[];
  onEdit: (candidate: Candidate) => void;
  onDelete: (candidate: Candidate) => void;
}

export default function CandidatesTable({ candidates, onEdit, onDelete }: Props) {
  const { t } = useTranslation("common");
  const isEmpty = candidates.length === 0;

  return (
    <Table size="small">
      <TableHead>
        <TableRow>
          <TableCell>{t("candidates.fields.name")}</TableCell>
          <TableCell>{t("candidates.fields.dni")}</TableCell>
          <TableCell>{t("candidates.fields.role")}</TableCell>
          <TableCell>{t("candidates.fields.location")}</TableCell>
          <TableCell>{t("candidates.fields.status")}</TableCell>
          <TableCell>{t("candidates.fields.experience")}</TableCell>
          <TableCell>{t("candidates.fields.strength")}</TableCell>
          <TableCell>{t("candidates.fields.salaryRange")}</TableCell>
          <TableCell>{t("candidates.fields.notes")}</TableCell>
          <TableCell align="right">
            {t("candidates.table.actions")}
          </TableCell>
        </TableRow>
      </TableHead>

      <TableBody>
        {isEmpty ? (
          <TableRow>
            <TableCell colSpan={10}>
              <Typography variant="body2" color="text.secondary">
                {t("candidates.empty")}
              </Typography>
            </TableCell>
          </TableRow>
        ) : (
          candidates.map((c) => (
            <TableRow key={c.candidateId} hover>
              <TableCell>{c.name}</TableCell>
              <TableCell>{c.dni}</TableCell>
              <TableCell>{c.role}</TableCell>
              <TableCell>{c.location}</TableCell>
              <TableCell>{c.status}</TableCell>
              <TableCell>{c.experience ?? "-"}</TableCell>
              <TableCell>{c.strength ?? "-"}</TableCell>
              <TableCell>{c.salaryRange ?? "-"}</TableCell>
              <TableCell>{c.notes}</TableCell>
              <TableCell align="right">
                <IconButton size="small" onClick={() => onEdit(c)}>
                  <EditIcon fontSize="small" />
                </IconButton>
                <IconButton
                  size="small"
                  color="error"
                  onClick={() => onDelete(c)}
                >
                  <DeleteIcon fontSize="small" />
                </IconButton>
              </TableCell>
            </TableRow>
          ))
        )}
      </TableBody>
    </Table>
  );
}
