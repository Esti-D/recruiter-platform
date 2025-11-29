export default {
  // --- App & Navigation ---
  "app.title": "Recruiter Platform",
  "nav.offers": "Stellenangebote",
  "nav.candidates": "Kandidaten",
  "nav.processes": "Prozesse",
  "nav.roles": "Rollen",
  "nav.settings": "Einstellungen",

  // --- Kandidaten ---
  "candidates.title": "Kandidaten",
  "candidates.new": "Neuer Kandidat",
  "candidates.edit": "Kandidat bearbeiten",
  "candidates.create": "Erstellen",
  "candidates.saveChanges": "Änderungen speichern",
  "candidates.cancel": "Abbrechen",
  "candidates.confirmDelete":
    'Möchten Sie den Kandidaten "{{name}}" wirklich löschen?',

  "candidates.fields.name": "Name",
  "candidates.fields.dni": "ID-Nummer",
  "candidates.fields.role": "Rolle",
  "candidates.fields.location": "Standort",
  "candidates.fields.status": "Status",
  "candidates.fields.experience": "Erfahrung",
  "candidates.fields.strength": "Stärken",
  "candidates.fields.salaryRange": "Gehaltsbereich",
  "candidates.fields.notes": "Notizen",

  "candidates.status.OPEN_TO_LISTEN": "Offen für Angebote",
  "candidates.status.NOT_INTERESTED": "Kein Interesse",

  "candidates.table.actions": "Aktionen",
  "candidates.empty": "Keine Kandidaten gefunden.",

  // --- Angebote ---
  "offers.title": "Stellenangebote",
  "offers.new": "Neues Angebot",
  "offers.edit": "Angebot bearbeiten",
  "offers.create": "Erstellen",
  "offers.saveChanges": "Änderungen speichern",
  "offers.cancel": "Abbrechen",
  "offers.empty": "Keine Angebote verfügbar.",
  "offers.confirmDelete":
    'Möchten Sie das Angebot "{{role}}" von "{{company}}" wirklich löschen?',

  "offers.fields.companyName": "Firma",
  "offers.fields.contactPerson": "Ansprechpartner",
  "offers.fields.role": "Rolle",
  "offers.fields.modality": "Arbeitsmodell",
  "offers.fields.location": "Standort",
  "offers.fields.description": "Beschreibung",
  "offers.fields.createdAt": "Erstellt am",

  "offers.modality.REMOTE": "Remote",
  "offers.modality.HYBRID": "Hybrid",
  "offers.modality.ONSITE": "Vor Ort",

  "offers.table.actions": "Aktionen",
  "offers.table.edit": "Angebot bearbeiten",
  "offers.table.delete": "Angebot löschen",

  // --- Rollen ---
  "roles.title": "Rollen",
  "roles.new": "Neue Rolle",
  "roles.edit": "Rolle bearbeiten",
  "roles.create": "Erstellen",
  "roles.saveChanges": "Änderungen speichern",
  "roles.cancel": "Abbrechen",
  "roles.empty": "Keine Rollen verfügbar.",

  "roles.reassignTitle": "Rolle in Verwendung",
  "roles.reassignText":
    'Die Rolle "{{name}}" wird derzeit verwendet. Bitte wählen Sie eine Ersatzrolle:',
  "roles.reassign": "Neu zuweisen und löschen",

  "roles.fields.name": "Name",
  "roles.fields.createdAt": "Erstellt am",
  "roles.fields.replacement": "Ersatzrolle",

  "roles.table.actions": "Aktionen",
  "roles.errorSaving": "Fehler beim Speichern der Rolle.",

  // --- Prozesse ---
  "processes.title": "Prozesse",
  "processes.new": "Neuer Prozess",
  "processes.create": "Erstellen",
  "processes.cancel": "Abbrechen",
  "processes.empty": "Keine Prozesse verfügbar.",
  "processes.confirmClose":
    'Möchten Sie den Prozess "{{id}}" wirklich schließen?',
  "processes.reload": "Prozesse neu laden",

  "processes.fields.processId": "Prozess-ID",
  "processes.fields.offer": "Stellenangebot",
  "processes.fields.offerId": "Angebots-ID",
  "processes.fields.roleOffer": "Rolle des Angebots",
  "processes.fields.similarRoles": "Ähnliche Rollen",
  "processes.fields.similarRolesHint": "Liste durch Kommas trennen",
  "processes.fields.recruiter": "Recruiter",
  "processes.fields.status": "Status",
  "processes.fields.notes": "Notizen",
  "processes.fields.createdAt": "Erstellt am",
  "processes.fields.closedAt": "Geschlossen am",
  "processes.fields.candidatesCount": "Kandidaten",

  "processes.table.actions": "Aktionen",

  "processes.back": "Zurück",
  "processes.detailTitle": "Prozess {{id}}",
  "processes.detailCandidatesTitle": "Kandidaten in diesem Prozess",
  "processes.saveCandidates": "Änderungen speichern",

  "processes.candidates.fields.name": "Name",
  "processes.candidates.fields.role": "Rolle",
  "processes.candidates.fields.experience": "Erfahrung",
  "processes.candidates.fields.strength": "Stärken",
  "processes.candidates.fields.salaryRange": "Gehaltsbereich",
  "processes.candidates.fields.state": "Status",
  "processes.candidates.fields.notes": "Notizen",

  "processes.saveProcess": "Prozess speichern",
  "processes.generateCandidates": "Kandidatenliste generieren",
  "processes.similarRoles.title": "Ähnliche Rollen",

  "processes.candidateStatus.INITIAL": "Initial",
  "processes.candidateStatus.IN_PROGRESS": "In Bearbeitung",
  "processes.candidateStatus.REJECTED": "Abgelehnt",
  "processes.candidateStatus.APPROVED": "Genehmigt"
};
