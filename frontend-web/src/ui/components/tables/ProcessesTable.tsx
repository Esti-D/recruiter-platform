// src/ui/components/tables/ProcessesTable.tsx
import { Process } from "../../../domain/processes";
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
  IconButton,
  Chip
} from "@mui/material";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import CloseIcon from "@mui/icons-material/Close";
import { useTranslation } from "react-i18next";

interface Props {
  processes: Process[];
  onOpen: (process: Process) => void;
  onClose: (process: Process) => void;
}

export default function ProcessesTable({ processes, onOpen, onClose }: Props) {
  const { t } = useTranslation("common");
  const isEmpty = processes.length === 0;

  return (
    <Table size="small">
      <TableHead>
        <TableRow>
          <TableCell>{t("processes.fields.processId")}</TableCell>
          <TableCell>{t("processes.fields.offerId")}</TableCell>
          <TableCell>{t("processes.fields.roleOffer")}</TableCell>
          <TableCell>{t("processes.fields.recruiter")}</TableCell>
          <TableCell>{t("processes.fields.status")}</TableCell>
          <TableCell>{t("processes.fields.createdAt")}</TableCell>
          <TableCell>{t("processes.fields.closedAt")}</TableCell>
          <TableCell>{t("processes.fields.candidatesCount")}</TableCell>
          <TableCell align="right">{t("processes.table.actions")}</TableCell>
        </TableRow>
      </TableHead>

      <TableBody>
        {isEmpty ? (
          <TableRow>
            <TableCell colSpan={9}>
              <Typography variant="body2" color="text.secondary">
                {t("processes.empty")}
              </Typography>
            </TableCell>
          </TableRow>
        ) : (
          processes.map((p) => (
            <TableRow key={p.processId} hover>
              <TableCell>{p.processId}</TableCell>
              <TableCell>{p.offerId}</TableCell>
              <TableCell>{p.roleOffer}</TableCell>
              <TableCell>{p.recruiter}</TableCell>
              <TableCell>
                <Chip
                  size="small"
                  label={t(`processes.status.${p.status}`, p.status)}
                  color={
                    p.status === "OPEN"
                      ? "success"
                      : p.status === "PAUSED"
                      ? "warning"
                      : "default"
                  }
                />
              </TableCell>
              <TableCell>{p.createdAt}</TableCell>
              <TableCell>{p.closedAt ?? "-"}</TableCell>
              <TableCell>{p.candidates?.length ?? 0}</TableCell>
              <TableCell align="right">
                <IconButton size="small" onClick={() => onOpen(p)}>
                  <OpenInNewIcon fontSize="small" />
                </IconButton>
                {p.status === "OPEN" && (
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => onClose(p)}
                  >
                    <CloseIcon fontSize="small" />
                  </IconButton>
                )}
              </TableCell>
            </TableRow>
          ))
        )}
      </TableBody>
    </Table>
  );
}

