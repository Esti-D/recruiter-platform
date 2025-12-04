// src/i18n/ga.ts
export default {
  // --- App & navegación ---
  "app.title": "Recruiter Platform",
  "nav.offers": "Tairiscintí",
  "nav.candidates": "Iarrthóirí",
  "nav.processes": "Próisis",
  "nav.roles": "Róil",
  "nav.settings": "Socruithe",

  // --- Candidatos ---
  "candidates.title": "Iarrthóirí",
  "candidates.new": "Iarrthóir nua",
  "candidates.edit": "Cuir iarrthóir in eagar",
  "candidates.create": "Cruthaigh",
  "candidates.saveChanges": "Sábháil athruithe",
  "candidates.cancel": "Cealaigh",
  "candidates.confirmDelete":
    'An bhfuil tú cinnte gur mhaith leat an t-iarrthóir "{{name}}" a scriosadh?',

  // Campos de candidatos
  "candidates.fields.name": "Ainm",
  "candidates.fields.dni": "Uimhir aitheantais",
  "candidates.fields.role": "Ról",
  "candidates.fields.location": "Suíomh",
  "candidates.fields.status": "Stádas",
  "candidates.fields.experience": "Taithí",
  "candidates.fields.strength": "Láidreacht",
  "candidates.fields.salaryRange": "Raon tuarastail",
  "candidates.fields.notes": "Nótaí",

  // Estados del candidato
  "candidates.status.OPEN_TO_LISTEN": "Oscailte do thairiscintí",
  "candidates.status.NOT_INTERESTED": "Gan suim",

  "candidates.table.actions": "Gníomhartha",
  "candidates.empty": "Níl aon iarrthóirí ar fáil.",

  // --- Ofertas ---
  "offers.title": "Tairiscintí",
  "offers.new": "Tairiscint nua",
  "offers.edit": "Cuir tairiscint in eagar",
  "offers.create": "Cruthaigh",
  "offers.saveChanges": "Sábháil athruithe",
  "offers.cancel": "Cealaigh",
  "offers.empty": "Níl aon tairiscintí ar fáil.",
  "offers.confirmDelete":
    'An bhfuil tú cinnte gur mhaith leat an tairiscint "{{role}}" ó "{{company}}" a scriosadh?',

  // Campos de ofertas
  "offers.fields.companyName": "Comhlacht",
  "offers.fields.contactPerson": "Duine teagmhála",
  "offers.fields.role": "Ról",
  "offers.fields.modality": "Modh oibre",
  "offers.fields.location": "Suíomh",
  "offers.fields.description": "Cur síos",
  "offers.fields.createdAt": "Cruthaithe ar",

  // Modalidades
  "offers.modality.REMOTE": "Fad-oibre",
  "offers.modality.HYBRID": "Hibrid",
  "offers.modality.ONSITE": "Ar an láthair",

  "offers.table.actions": "Gníomhartha",
  "offers.table.edit": "Cuir tairiscint in eagar",
  "offers.table.delete": "Scrios tairiscint",

  // --- Roles ---
  "roles.title": "Róil",
  "roles.new": "Ról nua",
  "roles.edit": "Cuir ról in eagar",
  "roles.create": "Cruthaigh",
  "roles.saveChanges": "Sábháil athruithe",
  "roles.cancel": "Cealaigh",
  "roles.empty": "Níl aon róil ar fáil.",

  "roles.reassignTitle": "Ról in úsáid",
  "roles.reassignText":
    'Tá an ról "{{name}}" in úsáid faoi láthair. Roghnaigh ról nua mar ionadach:',
  "roles.reassign": "Athshann agus scrios",

  // Campos de roles
  "roles.fields.name": "Ainm",
  "roles.fields.createdAt": "Cruthaithe ar",
  "roles.fields.replacement": "Ról ionaid",

  "roles.table.actions": "Gníomhartha",
  "roles.errorSaving": "Earráid agus an ról á shábháil.",

  // --- Procesos ---
  "processes.title": "Próisis",
  "processes.new": "Próiseas nua",
  "processes.create": "Cruthaigh",
  "processes.cancel": "Cealaigh",
  "processes.empty": "Níl aon phróisis ar fáil.",
  "processes.confirmClose":
    'An bhfuil tú cinnte gur mhaith leat an próiseas "{{id}}" a dhúnadh?',
  "processes.reload": "Athlódáil próisis",

  // Campos de procesos
  "processes.fields.processId": "ID próisis",
  "processes.fields.offer": "Tairiscint",
  "processes.fields.offerId": "ID tairisceana",
  "processes.fields.roleOffer": "Ról na tairisceana",
  "processes.fields.similarRoles": "Róil chosúla",
  "processes.fields.similarRolesHint": "Scar le camóga",
  "processes.fields.recruiter": "Earcróir",
  "processes.fields.status": "Stádas",
  "processes.fields.notes": "Nótaí",
  "processes.fields.createdAt": "Cruthaithe ar",
  "processes.fields.closedAt": "Dúnta ar",
  "processes.fields.candidatesCount": "Iarrthóirí",

  "processes.table.actions": "Gníomhartha",

  "processes.back": "Ar ais chuig próisis",
  "processes.detailTitle": "Próiseas {{id}}",
  "processes.detailCandidatesTitle": "Iarrthóirí sa phróiseas seo",
  "processes.saveCandidates": "Sábháil athruithe",

  // Campos candidatos dentro del proceso
  "processes.candidates.fields.name": "Ainm",
  "processes.candidates.fields.role": "Ról",
  "processes.candidates.fields.experience": "Taithí",
  "processes.candidates.fields.strength": "Láidreacht",
  "processes.candidates.fields.salaryRange": "Raon tuarastail",
  "processes.candidates.fields.state": "Stádas",
  "processes.candidates.fields.notes": "Nótaí",

  "processes.saveProcess": "Sábháil próiseas",
  "processes.generateCandidates": "Giniúint liosta iarrthóirí",
  "processes.similarRoles.title": "Róil chosúla",

  // Estados del candidato en un proceso
  "processes.candidateStatus.INITIAL": "Tosaigh",
  "processes.candidateStatus.IN_PROGRESS": "Ar siúl",
  "processes.candidateStatus.REJECTED": "Diúltaithe",
  "processes.candidateStatus.APPROVED": "Ceadaithe",
  "nav.workflow": "Workflow",
  "workflow.title": "Sreabhadh bailíochtaithe",
  "workflow.loading": "Míreanna ar feitheamh á lódáil…",
  "workflow.candidates": "Iarrthóirí ar feitheamh",
  "workflow.candidates_sub": "Cruthaithe ag iarrthóirí, ag fanacht lena n-athbhreithniú",
  "workflow.no_candidates": "Níl aon iarrthóirí ar feitheamh.",
  "workflow.created_by_candidate": "Cruthú iarrthóra",
  "workflow.offers": "Tairiscintí ar feitheamh",
  "workflow.offers_sub": "Cruthaithe ag cuideachtaí, ag fanacht lena n-athbhreithniú",
  "workflow.no_offers": "Níl aon tairiscintí ar feitheamh.",
  "workflow.created_by_company": "Cruthú tairisceana",
  "workflow.validate": "Bailíochtú",

};
