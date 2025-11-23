// src/ui/components/tables/ProcessCandidatesTable.tsx
import { ProcessCandidate } from "../../../domain/processes";
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TextField
} from "@mui/material";
import { useTranslation } from "react-i18next";

interface Props {
  candidates: ProcessCandidate[];
  onChange: (candidates: ProcessCandidate[]) => void;
  disabled?: boolean;
}

export default function ProcessCandidatesTable({
  candidates,
  onChange,
  disabled
}: Props) {
  const { t } = useTranslation("common");

  const handleChange =
    (index: number, field: keyof ProcessCandidate) =>
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const value = event.target.value;
      const updated = candidates.map((c, i) =>
        i === index ? { ...c, [field]: value } : c
      );
      onChange(updated);
    };

  return (
    <Table size="small">
      <TableHead>
        <TableRow>
          <TableCell>{t("processes.candidates.fields.name")}</TableCell>
          <TableCell>{t("processes.candidates.fields.role")}</TableCell>
          <TableCell>{t("processes.candidates.fields.experience")}</TableCell>
          <TableCell>{t("processes.candidates.fields.strength")}</TableCell>
          <TableCell>{t("processes.candidates.fields.salaryRange")}</TableCell>
          <TableCell>{t("processes.candidates.fields.state")}</TableCell>
          <TableCell>{t("processes.candidates.fields.notes")}</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {candidates.map((c, index) => (
          <TableRow key={c.candidateId}>
            <TableCell>{c.name}</TableCell>
            <TableCell>{c.role}</TableCell>

            <TableCell>
              <TextField
                value={c.experience ?? ""}
                onChange={handleChange(index, "experience")}
                size="small"
                fullWidth
                disabled={disabled}
              />
            </TableCell>

            <TableCell>
              <TextField
                value={c.strength ?? ""}
                onChange={handleChange(index, "strength")}
                size="small"
                fullWidth
                disabled={disabled}
              />
            </TableCell>

            <TableCell>
              <TextField
                value={c.salaryRange ?? ""}
                onChange={handleChange(index, "salaryRange")}
                size="small"
                fullWidth
                disabled={disabled}
              />
            </TableCell>

            <TableCell>
              <TextField
                value={c.state ?? ""}
                onChange={handleChange(index, "state")}
                size="small"
                fullWidth
                disabled={disabled}
              />
            </TableCell>

            <TableCell>
              <TextField
                value={c.notes ?? ""}
                onChange={handleChange(index, "notes")}
                size="small"
                fullWidth
                disabled={disabled}
                multiline
                minRows={1}
              />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
