// src/i18n/index.ts
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

// Idiomas externos (ficheros que hemos ido creando)
import es from "./es";
import fr from "./fr";
import de from "./de";
import it from "./it";
import eu from "./eu";
import ca from "./ca";
import ga from "./ga"; // gaélico (irlandés)
import rm from "./rm"; // romanche

// Inglés lo dejamos definido aquí mismo
const en = {
  "app.title": "Recruiter Platform",
  "nav.offers": "Offers",
  "nav.candidates": "Candidates",
  "nav.processes": "Processes",
  "nav.roles": "Roles",
  "nav.settings": "Settings",

  // ---- Candidates ----
  "candidates.title": "Candidates",
  "candidates.new": "New candidate",
  "candidates.edit": "Edit candidate",
  "candidates.create": "Create",
  "candidates.saveChanges": "Save changes",
  "candidates.cancel": "Cancel",
  "candidates.confirmDelete":
    'Are you sure you want to delete candidate "{{name}}"?',

  "candidates.fields.name": "Name",
  "candidates.fields.dni": "ID number",
  "candidates.fields.role": "Role",
  "candidates.fields.location": "Location",
  "candidates.fields.status": "Status",
  "candidates.fields.experience": "Experience",
  "candidates.fields.strength": "Strength",
  "candidates.fields.salaryRange": "Salary range",
  "candidates.fields.notes": "Notes",

  "candidates.table.actions": "Actions",
  "candidates.empty": "No candidates found.",

  // Candidate status
  "candidates.status.OPEN_TO_LISTEN": "Open to listen",
  "candidates.status.NOT_INTERESTED": "Not interested",

  // ---- Offers page ----
  "offers.title": "Offers",
  "offers.new": "New offer",
  "offers.edit": "Edit offer",
  "offers.create": "Create",
  "offers.saveChanges": "Save changes",
  "offers.cancel": "Cancel",
  "offers.empty": "No offers found.",
  "offers.confirmDelete":
    'Are you sure you want to delete the offer "{{role}}" at "{{company}}"?',

  "offers.fields.companyName": "Company",
  "offers.fields.contactPerson": "Contact person",
  "offers.fields.role": "Role",
  "offers.fields.modality": "Modality",
  "offers.fields.location": "Location",
  "offers.fields.description": "Description",
  "offers.fields.createdAt": "Created at",

  // Modality
  "offers.modality.REMOTE": "Remote",
  "offers.modality.HYBRID": "Hybrid",
  "offers.modality.ONSITE": "On site",

  "offers.table.actions": "Actions",
  "offers.table.edit": "Edit offer",
  "offers.table.delete": "Delete offer",

  // ---- Roles page ----
  "roles.title": "Roles",
  "roles.new": "New role",
  "roles.edit": "Edit role",
  "roles.create": "Create",
  "roles.saveChanges": "Save changes",
  "roles.cancel": "Cancel",
  "roles.empty": "No roles found.",

  "roles.reassignTitle": "Role in use",
  "roles.reassignText":
    'The role "{{name}}" is currently in use. Choose a replacement role:',
  "roles.reassign": "Reassign and delete",

  "roles.fields.name": "Name",
  "roles.fields.createdAt": "Created at",
  "roles.fields.replacement": "Replacement role",

  "roles.table.actions": "Actions",
  "roles.errorSaving": "Error saving role.",

  // ---- Processes page ----
  "processes.title": "Processes",
  "processes.new": "New process",
  "processes.create": "Create",
  "processes.cancel": "Cancel",
  "processes.empty": "No processes found.",
  "processes.confirmClose":
    'Are you sure you want to close process "{{id}}"?',
  "processes.reload": "Reload processes",

  "processes.fields.processId": "Process ID",
  "processes.fields.offer": "Offer",
  "processes.fields.offerId": "Offer ID",
  "processes.fields.roleOffer": "Role (offer)",
  "processes.fields.similarRoles": "Similar roles",
  "processes.fields.similarRolesHint": "Comma separated list of similar roles",
  "processes.fields.recruiter": "Recruiter",
  "processes.fields.status": "Status",
  "processes.fields.notes": "Notes",
  "processes.fields.createdAt": "Created at",
  "processes.fields.closedAt": "Closed at",
  "processes.fields.candidatesCount": "Candidates",

  "processes.table.actions": "Actions",

  "processes.back": "Back to processes",
  "processes.detailTitle": "Process {{id}}",
  "processes.detailCandidatesTitle": "Candidates in this process",
  "processes.saveCandidates": "Save candidates changes",

  "processes.candidates.fields.name": "Name",
  "processes.candidates.fields.role": "Role",
  "processes.candidates.fields.experience": "Experience",
  "processes.candidates.fields.strength": "Strength",
  "processes.candidates.fields.salaryRange": "Salary range",
  "processes.candidates.fields.state": "State",
  "processes.candidates.fields.notes": "Notes",

  "processes.saveProcess": "Save process",
  "processes.generateCandidates": "Generate candidates list",
  "processes.similarRoles.title": "Similar roles",

  // Candidate status inside process
  "processes.candidateStatus.INITIAL": "Initial",
  "processes.candidateStatus.IN_PROGRESS": "In progress",
  "processes.candidateStatus.REJECTED": "Rejected",
  "processes.candidateStatus.APPROVED": "Approved",

  "nav.workflow": "Workflow",

  "workflow.title": "Validation workflow",
  "workflow.loading": "Loading pending items…",
  "workflow.candidates": "Pending candidates",
  "workflow.candidates_sub": "Created by candidates, waiting for review",
  "workflow.no_candidates": "No pending candidates.",
  "workflow.created_by_candidate": "Candidate profile creation",
  "workflow.offers": "Pending offers",
  "workflow.offers_sub": "Created by companies, waiting for review",
  "workflow.no_offers": "No pending offers.",
  "workflow.created_by_company": "Offer creation",
  "workflow.validate": "Validate",


};

i18n.use(initReactI18next).init({
  resources: {
    en: { common: en },
    es: { common: es },
    fr: { common: fr },
    de: { common: de },
    it: { common: it },
    eu: { common: eu },
    ca: { common: ca },
    ga: { common: ga },
    rm: { common: rm }
  },
  lng: "en",
  fallbackLng: "en",
  supportedLngs: ["en", "es", "eu", "ca", "fr", "de", "it", "ga", "rm"],
  ns: ["common"],
  defaultNS: "common",
  interpolation: { escapeValue: false }
});

export default i18n;
