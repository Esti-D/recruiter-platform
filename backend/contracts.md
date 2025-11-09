# Contratos JSON — Backend v1.0-desktop

## 1. Offers Service
**POST /offers**
Crea una oferta.

Request:
{
  "offerId": "string",
  "role": "string",
  "tags": ["string"],
  "createdBy": "string"
}

Response:
{
  "offerId": "string",
  "status": "CREATED"
}


## 2. Process Service
**POST /process**
Crea un proceso asociado a una oferta.

Request:
{
  "offerId": "string"
}

Response:
{
  "processId": "string",
  "offerId": "string",
  "status": "READY"
}


**POST /process/{processId}/snapshot:generate**
Genera snapshot de candidatos por rol.

Request:
{
  "role": "string"
}

Response:
{
  "snapshotId": "string",
  "status": "GENERATING"
}


**GET /process/{processId}/snapshot**
Obtiene el snapshot actual con filtros y orden.

Response:
{
  "items": [
    { "candidateId": "string", "fitScore": "number", "tags": ["string"] }
  ],
  "meta": { "count": "number", "filters": "object" }
}


**PATCH /process/{processId}/snapshot**
Edita o actualiza información del snapshot.

Request:
{
  "edits": [
    { "candidateId": "string", "action": "string", "value": "any" }
  ]
}

Response:
{
  "snapshotId": "string",
  "version": "number"
}


## 3. Candidates Service
**GET /candidates**
Consulta candidatos filtrados.

Query params:
?role=string&skills=string&limit=number&cursor=string

Response:
{
  "items": [
    {
      "candidateId": "string",
      "name": "string",
      "role": "string",
      "skills": ["string"]
    }
  ],
  "cursor": "string"
}
