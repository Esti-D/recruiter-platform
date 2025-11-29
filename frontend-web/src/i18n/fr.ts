// src/i18n/fr.ts
export default {
  // --- Application & navigation ---
  "app.title": "Recruiter Platform",
  "nav.offers": "Offres",
  "nav.candidates": "Candidats",
  "nav.processes": "Processus",
  "nav.roles": "Rôles",
  "nav.settings": "Paramètres",

  // --- Candidats ---
  "candidates.title": "Candidats",
  "candidates.new": "Nouveau candidat",
  "candidates.edit": "Modifier le candidat",
  "candidates.create": "Créer",
  "candidates.saveChanges": "Enregistrer les modifications",
  "candidates.cancel": "Annuler",
  "candidates.confirmDelete":
    'Êtes-vous sûr de vouloir supprimer le candidat « {{name}} » ?',

  // Champs candidats
  "candidates.fields.name": "Nom",
  "candidates.fields.dni": "Numéro d’identification",
  "candidates.fields.role": "Rôle",
  "candidates.fields.location": "Localisation",
  "candidates.fields.status": "Statut",
  "candidates.fields.experience": "Expérience",
  "candidates.fields.strength": "Points forts",
  "candidates.fields.salaryRange": "Fourchette de salaire",
  "candidates.fields.notes": "Notes",

  // Statuts du candidat
  "candidates.status.OPEN_TO_LISTEN": "Ouvert aux opportunités",
  "candidates.status.NOT_INTERESTED": "Pas intéressé",

  "candidates.table.actions": "Actions",
  "candidates.empty": "Aucun candidat disponible.",

  // --- Offres ---
  "offers.title": "Offres",
  "offers.new": "Nouvelle offre",
  "offers.edit": "Modifier l’offre",
  "offers.create": "Créer",
  "offers.saveChanges": "Enregistrer les modifications",
  "offers.cancel": "Annuler",
  "offers.empty": "Aucune offre disponible.",
  "offers.confirmDelete":
    'Êtes-vous sûr de vouloir supprimer l’offre « {{role}} » de l’entreprise « {{company}} » ?',

  // Champs offres
  "offers.fields.companyName": "Entreprise",
  "offers.fields.contactPerson": "Personne de contact",
  "offers.fields.role": "Rôle",
  "offers.fields.modality": "Modalité",
  "offers.fields.location": "Localisation",
  "offers.fields.description": "Description",
  "offers.fields.createdAt": "Date de création",

  // Modalités
  "offers.modality.REMOTE": "Télétravail",
  "offers.modality.HYBRID": "Hybride",
  "offers.modality.ONSITE": "Sur site",

  "offers.table.actions": "Actions",
  "offers.table.edit": "Modifier l’offre",
  "offers.table.delete": "Supprimer l’offre",

  // --- Rôles ---
  "roles.title": "Rôles",
  "roles.new": "Nouveau rôle",
  "roles.edit": "Modifier le rôle",
  "roles.create": "Créer",
  "roles.saveChanges": "Enregistrer les modifications",
  "roles.cancel": "Annuler",
  "roles.empty": "Aucun rôle disponible.",

  "roles.reassignTitle": "Rôle utilisé",
  "roles.reassignText":
    'Le rôle « {{name}} » est actuellement utilisé. Veuillez choisir un rôle de remplacement :',
  "roles.reassign": "Réaffecter et supprimer",

  // Champs rôles
  "roles.fields.name": "Nom",
  "roles.fields.createdAt": "Date de création",
  "roles.fields.replacement": "Rôle de remplacement",

  "roles.table.actions": "Actions",
  "roles.errorSaving": "Erreur lors de l’enregistrement du rôle.",

  // --- Processus ---
  "processes.title": "Processus",
  "processes.new": "Nouveau processus",
  "processes.create": "Créer",
  "processes.cancel": "Annuler",
  "processes.empty": "Aucun processus disponible.",
  "processes.confirmClose":
    'Êtes-vous sûr de vouloir fermer le processus « {{id}} » ?',
  "processes.reload": "Recharger les processus",

  // Champs processus
  "processes.fields.processId": "ID du processus",
  "processes.fields.offer": "Offre",
  "processes.fields.offerId": "ID de l’offre",
  "processes.fields.roleOffer": "Rôle de l’offre",
  "processes.fields.similarRoles": "Rôles similaires",
  "processes.fields.similarRolesHint": "Liste séparée par des virgules",
  "processes.fields.recruiter": "Recruteur",
  "processes.fields.status": "Statut",
  "processes.fields.notes": "Notes",
  "processes.fields.createdAt": "Date de création",
  "processes.fields.closedAt": "Date de clôture",
  "processes.fields.candidatesCount": "Candidats",

  "processes.table.actions": "Actions",

  "processes.back": "Retour aux processus",
  "processes.detailTitle": "Processus {{id}}",
  "processes.detailCandidatesTitle": "Candidats dans ce processus",
  "processes.saveCandidates": "Enregistrer les modifications",

  // Champs candidats dans le processus
  "processes.candidates.fields.name": "Nom",
  "processes.candidates.fields.role": "Rôle",
  "processes.candidates.fields.experience": "Expérience",
  "processes.candidates.fields.strength": "Points forts",
  "processes.candidates.fields.salaryRange": "Fourchette de salaire",
  "processes.candidates.fields.state": "Statut",
  "processes.candidates.fields.notes": "Notes",

  "processes.saveProcess": "Enregistrer le processus",
  "processes.generateCandidates": "Générer la liste de candidats",
  "processes.similarRoles.title": "Rôles similaires",

  // Statuts du candidat dans le processus
  "processes.candidateStatus.INITIAL": "Initial",
  "processes.candidateStatus.IN_PROGRESS": "En cours",
  "processes.candidateStatus.REJECTED": "Rejeté",
  "processes.candidateStatus.APPROVED": "Validé"
};
