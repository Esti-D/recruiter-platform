// src/i18n/index.ts
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

const resources = {
  en: {
    common: {
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
      "candidates.confirmDelete": "Are you sure you want to delete candidate \"{{name}}\"?",

      // Fields
      "candidates.fields.name": "Name",
      "candidates.fields.dni": "ID number",
      "candidates.fields.role": "Role",
      "candidates.fields.location": "Location",
      "candidates.fields.status": "Status",
      "candidates.fields.experience": "Experience",
      "candidates.fields.strength": "Strength",
      "candidates.fields.salaryRange": "Salary range",
      "candidates.fields.notes": "Notes",

      // Candidates table
      "candidates.table.actions": "Actions",
      "candidates.empty": "No candidates found.",
  
      // ---- Offers page ----
       "offers.title": "Offers",
      "offers.new": "New offer",
      "offers.edit": "Edit offer",
      "offers.create": "Create",
      "offers.saveChanges": "Save changes",
      "offers.cancel": "Cancel",
      "offers.empty": "No offers found.",
      "offers.confirmDelete": "Are you sure you want to delete the offer \"{{role}}\" at \"{{company}}\"?",

      "offers.fields.companyName": "Company",
      "offers.fields.contactPerson": "Contact person",
      "offers.fields.role": "Role",
      "offers.fields.modality": "Modality",
      "offers.fields.location": "Location",
      "offers.fields.description": "Description",
      "offers.fields.createdAt": "Created at",

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

      // Reassign logic
      "roles.reassignTitle": "Role in use",
      "roles.reassignText": "The role \"{{name}}\" is currently in use. Choose a replacement role:",
      "roles.reassign": "Reassign and delete",

      // Fields
      "roles.fields.name": "Name",
      "roles.fields.createdAt": "Created at",
      "roles.fields.replacement": "Replacement role",

      // Table
      "roles.table.actions": "Actions",
      "roles.errorSaving": "Error saving role.",


            // ---- Processes page ----
      "processes.title": "Processes",
      "processes.new": "New process",
      "processes.create": "Create",
      "processes.cancel": "Cancel",
      "processes.empty": "No processes found.",
      "processes.confirmClose": "Are you sure you want to close process \"{{id}}\"?",
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

      // Processes detail
      "processes.back": "Back to processes",
      "processes.detailTitle": "Process {{id}}",
      "processes.detailCandidatesTitle": "Candidates in this process",
      "processes.saveCandidates": "Save candidates changes",

      "processes.candidates.fields.name": "Name",
      "processes.candidates.fields.role": "Role",
      "processes.candidates.fields.experience": "Experience",
      "processes.candidates.fields.strength": "Strength",
      "processes.candidates.fields.salaryRange": "Salary range",

      "processes.saveProcess": "Save process",
      "processes.generateCandidates": "Generate candidates list",
      "processes.similarRoles.title": "Similar roles",

      "processes.candidates.fields.state": "State",
      "processes.candidates.fields.notes": "Notes"

    }
  }
};

i18n.use(initReactI18next).init({
  resources,
  lng: "en",
  fallbackLng: "en",
  supportedLngs: ["en", "es", "eu", "ca", "fr", "de", "it", "ga", "rm"],
  ns: ["common"],
  defaultNS: "common",
  interpolation: { escapeValue: false }
});

export default i18n;
