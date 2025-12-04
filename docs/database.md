# Database Model – DynamoDB

This document describes the data model used by the Recruiter Platform.  
All data is stored in **Amazon DynamoDB**, using one table per domain:

- `ROLES_TABLE`
- `CANDIDATES_TABLE`
- `OFFERS_TABLE`
- `PROCESSES_TABLE`

Each table uses a simple partition key (no sort key), and items follow a JSON-like schema documented below.

---

## 1. Overview

DynamoDB was chosen because it provides:

- fully managed, serverless architecture  
- pay-per-use cost model  
- fast access by primary key  
- flexible schema for evolving domains  

Each table stores one type of entity, and the **process table embeds candidate lists** inside the process record.

---

## 2. Tables and Schemas

Below are the tables exactly as used by the backend code.

---

## 2.1 ROLE Table

**Partition key:** `roleId`

Represents a job role or position in the system.

### Fields

| Field       | Type     | Description                           |
|-------------|----------|---------------------------------------|
| `roleId`    | string   | Unique identifier                     |
| `name`      | string   | Name of the role                      |
| `createdAt` | string   | ISO timestamp                         |

### Notes
- Roles can only be deleted if they are not referenced by offers or candidates.
- The system supports **role reassignment** before deletion.

---

## 2.2 CANDIDATE Table

**Partition key:** `candidateId`

Represents an individual candidate and all associated metadata.

### Fields

| Field         | Type     | Description                                 |
|---------------|----------|---------------------------------------------|
| `candidateId` | string   | Unique identifier                            |
| `name`        | string   | Full name                                    |
| `dni`         | string   | National ID (treated as a string)            |
| `role`        | string   | Associated roleId                             |
| `location`    | string   | Geographic location                          |
| `status`      | string   | Status of the candidate workflow             |
| `workflow`    | string   | Workflow state (e.g. CREATED)                |
| `notes`       | string   | Recruiter notes                              |
| `experience`  | number   | Years of experience                          |
| `strength`    | string   | Summary of strengths                         |
| `salaryRange` | string   | Salary expectations                          |
| `userOwnerId` | string   | Cognito user ID when the candidate is user-owned |
| `createdAt`   | string   | ISO timestamp                                |
| `updatedAt`   | string   | ISO timestamp (on update)                    |

### Filtering
Supports filters on:

- `q` (name / text search)  
- `role`  
- `location`  
- `status`  
- `workflow`  

---

## 2.3 OFFER Table

**Partition key:** `offerId`

Represents a job offer posted by a company.

### Fields

| Field           | Type     | Description                                |
|-----------------|----------|--------------------------------------------|
| `offerId`       | string   | Unique identifier                          |
| `companyName`   | string   | Company offering the position              |
| `contactPerson` | string   | Hiring contact                              |
| `role`          | string   | Associated `roleId`                         |
| `modality`      | string   | Remote / hybrid / on-site                  |
| `location`      | string   | City, region                                |
| `description`   | string   | Job description                             |
| `workflow`      | string   | Workflow state (e.g. CREATED)               |
| `createdAt`     | string   | ISO timestamp                               |
| `updatedAt`     | string   | ISO timestamp (on update)                   |

### Filtering
Supports:

- `q`  
- `companyName`  
- `contactPerson`  
- `role`  
- `modality`  
- `location`  
- `workflow`  

---

## 2.4 PROCESS Table

**Partition key:** `processId`

Represents a hiring process opened for a specific offer.

### Fields

| Field           | Type       | Description                                          |
|-----------------|------------|------------------------------------------------------|
| `processId`     | string     | Unique identifier                                    |
| `offerId`       | string     | ID of the related offer                               |
| `roleOffer`     | string     | Role associated with the offer                        |
| `similarRoles`  | list       | List of role IDs considered compatible               |
| `recruiter`     | string     | User ID or recruiter name                             |
| `notes`         | string     | Free-form notes                                       |
| `status`        | string     | OPEN or CLOSED                                       |
| `createdAt`     | string     | ISO timestamp                                         |
| `closedAt`      | string     | ISO timestamp (when closed)                          |
| `candidates`    | list<map>  | List of compatible candidates generated for process  |

### Structure of candidate items inside a process

Each element inside the `candidates` list includes:

| Field         | Type   | Description                     |
|---------------|--------|---------------------------------|
| `candidateId` | string | ID of the candidate             |
| `name`        | string | Candidate name                  |
| `role`        | string | Role Id                         |
| `experience`  | number | Years of experience             |
| `strength`    | string | Strength summary                |
| `salaryRange` | string | Expected salary range           |

### Filtering

- `offerId`  
- `status`  

---

## 3. Relationships Between Tables

### Offers → Roles
Each offer references a role via `role`.

### Candidates → Roles
Each candidate references a role via `role`.

### Processes → Offers
A process always references an offer via `offerId`.

### Processes → Candidates (embedded)
Compatible candidates are stored **as a list inside the process item**, not in a separate table.

---

## 4. Design Considerations

- **One table per domain** provides clarity and easy querying.  
- **Embedded candidate lists** avoid the need for joins or secondary queries.  
- **Flexible schemas** allow new fields without migrations.  
- DynamoDB is ideal for this app because access patterns are:
  - simple lists  
  - get-by-id  
  - scan-with-filter  

### Possible future improvements

- Add GSIs to speed up search-heavy filters (role, workflow, etc.).  
- Add TTL fields where appropriate.  
- Introduce versioning to track historical changes.  

---