// src/ui/components/tables/RolesTable.tsx
import { Role } from "../../../domain/roles";
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
  roles: Role[];
  onEdit: (role: Role) => void;
  onDelete: (role: Role) => void;
}

export default function RolesTable({ roles, onEdit, onDelete }: Props) {
  const { t } = useTranslation("common");
  const isEmpty = roles.length === 0;

  return (
    <Table size="small">
      <TableHead>
        <TableRow>
          <TableCell>{t("roles.fields.name")}</TableCell>
          <TableCell>{t("roles.fields.createdAt")}</TableCell>
          <TableCell align="right">{t("roles.table.actions")}</TableCell>
        </TableRow>
      </TableHead>

      <TableBody>
        {isEmpty ? (
          <TableRow>
            <TableCell colSpan={3}>
              <Typography variant="body2" color="text.secondary">
                {t("roles.empty")}
              </Typography>
            </TableCell>
          </TableRow>
        ) : (
          roles.map((r) => (
            <TableRow key={r.roleId} hover>
              <TableCell>{r.name}</TableCell>
              <TableCell>{r.createdAt}</TableCell>
              <TableCell align="right">
                <IconButton size="small" onClick={() => onEdit(r)}>
                  <EditIcon fontSize="small" />
                </IconButton>

                <IconButton
                  size="small"
                  color="error"
                  onClick={() => onDelete(r)}
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
