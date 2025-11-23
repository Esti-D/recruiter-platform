// src/ui/components/tables/OffersTable.tsx
import { Offer } from "../../../domain/offers";
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  IconButton,
  Typography
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { useTranslation } from "react-i18next";

interface Props {
  offers: Offer[];
  onEdit: (offer: Offer) => void;
  onDelete: (offer: Offer) => void;
}

export default function OffersTable({ offers, onEdit, onDelete }: Props) {
  const { t } = useTranslation("common");
  const isEmpty = offers.length === 0;

  return (
    <Table size="small">
      <TableHead>
        <TableRow>
          <TableCell>{t("offers.fields.companyName")}</TableCell>
          <TableCell>{t("offers.fields.role")}</TableCell>
          <TableCell>{t("offers.fields.location")}</TableCell>
          <TableCell>{t("offers.fields.modality")}</TableCell>
          <TableCell>{t("offers.fields.contactPerson")}</TableCell>
          <TableCell>{t("offers.fields.createdAt")}</TableCell>
          <TableCell>{t("offers.fields.description")}</TableCell>
          <TableCell align="right">{t("offers.table.actions")}</TableCell>
        </TableRow>
      </TableHead>

      <TableBody>
        {isEmpty ? (
          <TableRow>
            <TableCell colSpan={8}>
              <Typography variant="body2" color="text.secondary">
                {t("offers.empty")}
              </Typography>
            </TableCell>
          </TableRow>
        ) : (
          offers.map((o) => (
            <TableRow key={o.offerId} hover>
              <TableCell>{o.companyName}</TableCell>
              <TableCell>{o.role}</TableCell>
              <TableCell>{o.location}</TableCell>
              <TableCell>{o.modality}</TableCell>
              <TableCell>{o.contactPerson}</TableCell>
              <TableCell>{o.createdAt}</TableCell>
              <TableCell>
                {o.description?.length > 80
                  ? o.description.slice(0, 80) + "…"
                  : o.description}
              </TableCell>
              <TableCell align="right">
                <IconButton
                  size="small"
                  onClick={() => onEdit(o)}
                  aria-label={t("offers.table.edit")}
                >
                  <EditIcon fontSize="small" />
                </IconButton>
                <IconButton
                  size="small"
                  color="error"
                  onClick={() => onDelete(o)}
                  aria-label={t("offers.table.delete")}
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
