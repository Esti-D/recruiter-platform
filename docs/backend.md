# Backend – Serverless API (AWS Lambda + API Gateway)

This document describes the backend of the Recruiter Platform, implemented as a fully serverless API using **AWS Lambda**, **Amazon API Gateway**, **Amazon DynamoDB**, and **Amazon Cognito**.  
The backend provides all business logic for managing roles, candidates, offers, and selection processes.

---

## 1. Overview

The backend is implemented using **two AWS Lambda functions**:

- **recruiter-core-lambda**: handles roles, candidates, offers and workflow views.
- **process-lambda**: handles selection processes.

Both Lambdas are exposed through **API Gateway** and use shared DynamoDB tables for persistence.

Key characteristics:

- 100% serverless backend  
- automatic scaling  
- no servers to maintain  
- stateless execution  
- authentication via Cognito JWT tokens  

---

## 2. API Structure

The API follows a **REST-style** design with resources grouped by domain:

- `/roles`
- `/candidates`
- `/offers`
- `/processes`
- `/workflow/candidates`
- `/workflow/offers`

Routing in API Gateway is configured so that:

- Requests to **roles, candidates and offers** are sent to `recruiter-core-lambda`.
- Requests to **processes** are sent to `process-lambda`.

Each Lambda:

1. Normalises the path (removing the stage from `rawPath` if present).  
2. Reads the HTTP method from the event.  
3. Dispatches the request to the corresponding service function.

---

## 3. Endpoints

### 3.1 Roles (recruiter-core-lambda)

Base path: `/roles`

| Method | Path                     | Description                                    |
|--------|--------------------------|------------------------------------------------|
| GET    | `/roles`                | List all roles. Supports optional search.      |
| POST   | `/roles`                | Create a new role.                             |
| GET    | `/roles/{roleId}`       | Retrieve a role by ID.                         |
| PATCH  | `/roles/{roleId}`       | Update role fields.                            |
| DELETE | `/roles/{roleId}`       | Delete a role (only if not in use).            |
| POST   | `/roles/{roleId}/reassign` | Reassign related entities to another role before deletion. |

---

### 3.2 Candidates (recruiter-core-lambda)

Base path: `/candidates`

| Method | Path                          | Description                                                                           |
|--------|-------------------------------|---------------------------------------------------------------------------------------|
| GET    | `/candidates`                 | List candidates. Supports filters `q`, `role`, `location`, `status`, `workflow`.     |
| POST   | `/candidates`                 | Create a new candidate.                                                              |
| GET    | `/candidates/{candidateId}`   | Retrieve candidate details.                                                          |
| PATCH  | `/candidates/{candidateId}`   | Update candidate.                                                                    |
| DELETE | `/candidates/{candidateId}`   | Delete candidate.                                                                    |

Filtering uses query string parameters and also applies access rules based on the caller’s role and user ID (headers `x-role` and `x-user-id`).

---

### 3.3 Offers (recruiter-core-lambda)

Base path: `/offers`

| Method | Path                      | Description                                                                     |
|--------|---------------------------|---------------------------------------------------------------------------------|
| GET    | `/offers`                | List job offers. Supports filters such as `q`, `companyName`, `contactPerson`, `role`, `modality`, `location`. |
| POST   | `/offers`                | Create a new offer.                                                             |
| GET    | `/offers/{offerId}`      | Retrieve offer details.                                                         |
| PATCH  | `/offers/{offerId}`      | Update offer.                                                                   |
| DELETE | `/offers/{offerId}`      | Delete offer.                                                                   |

---

### 3.4 Processes (process-lambda)

All process-related operations are handled by **process-lambda**.

Base path: `/processes`

| Method | Path                                      | Description                                                                |
|--------|-------------------------------------------|----------------------------------------------------------------------------|
| GET    | `/processes`                              | List processes. Supports filters `offerId` and `status`.                  |
| POST   | `/processes`                              | Create a new selection process.                                           |
| GET    | `/processes/{processId}`                  | Retrieve process details.                                                 |
| PATCH  | `/processes/{processId}`                  | Update process (notes, status, closing, etc.).                            |
| POST   | `/processes/{processId}/candidates:generate` | Generate compatible candidates for the given process and update it.    |

The generation endpoint loads the process from DynamoDB, applies matching rules using candidates and the offer information, and then stores the updated process including the generated candidate list.

---

### 3.5 Workflow Views (recruiter-core-lambda)

These endpoints provide a **workflow-oriented view** of entities, mainly for recruiter usage.

| Method | Path                   | Description                                                    |
|--------|------------------------|----------------------------------------------------------------|
| GET    | `/workflow/candidates` | List candidates filtered by their workflow state (e.g. CREATED). |
| GET    | `/workflow/offers`     | List offers filtered by their workflow state (e.g. CREATED).    |

Filtering is driven by the `workflow` field stored in the candidate / offer records.

---

## 4. Lambda Functions

### 4.1 recruiter-core-lambda

Responsible for:

- Routes for `/roles`, `/candidates`, `/offers`, `/workflow/*`.
- Normalising paths and handling CORS preflight (`OPTIONS`).
- Delegating to domain service modules:
  - `roles_service`
  - `candidates_service`
  - `offers_service`

Typical flow:

1. Normalise path from `rawPath`.
2. Read HTTP method.
3. Match `(route, method)` to a service (e.g. `list_candidates_service`, `update_role_service`, etc.).
4. Return a standard API Gateway response with CORS headers.

### 4.2 process-lambda

Responsible for:

- Routes for `/processes` and `/processes/{id}…`.
- Managing the full lifecycle of a selection process.
- Generating candidates for a process.

Flow:

1. Normalise `/processes` routes.
2. For each route/method, call one of:
   - `list_processes_service`
   - `create_process_service`
   - `get_process_service`
   - `update_process_service`
   - `generate_candidates_service`
3. Wrap the result into a standard API response.

---

### 4.3 Event Handling

Both Lambdas receive API Gateway events that may include:

- `rawPath`
- `requestContext.http.method` or `httpMethod`
- `pathParameters`
- `queryStringParameters`
- `headers`
- `body` (JSON string)

Service functions parse and validate the request body (using `json.loads`) and read filters from query parameters.

### 4.4 Error Handling

Both Lambdas follow a consistent error model, returning:

- **400** – invalid request data  
- **404** – entity not found  
- **409** – business conflict (e.g., trying to delete a role in use)  
- **500** – unexpected internal error  

Errors are returned in structured JSON:


{
  "error": "error_code",
  "message": "Human readable description"
}

---
## 5. DynamoDB Interactions

Both Lambdas access shared DynamoDB tables defined through environment variables:

- `CANDIDATES_TABLE`  
- `OFFERS_TABLE`  
- `ROLES_TABLE`  
- `PROCESSES_TABLE`  

Tables are accessed using the DynamoDB resource, for example:

    table = boto3.resource("dynamodb").Table("<table_name>")

### 5.1 Common Operations

- scan() – list or filter items  
- get_item() – retrieve a specific entity  
- put_item() – create or fully replace an item  
- update_item() – modify existing fields  
- delete_item() – remove an entity  

### 5.2 Access Patterns

- Roles → accessed by `roleId`.  
- Candidates → accessed by `candidateId`, with optional filters (`role`, `location`, `status`, `workflow`).  
- Offers → accessed by `offerId`, with optional filters (`companyName`, `role`, `modality`, `location`).  
- Processes → accessed by `processId`, storing the generated list of compatible candidates inside the item.  

A complete description of each table and its fields is included in `DATABASE.md`.

---

## 6. Authentication & Authorization

Authentication is performed using Amazon Cognito, and API Gateway validates JWT tokens through a Cognito Authorizer.

The frontend must include:

    Authorization: Bearer <token>

### 6.1 Additional Headers

The backend also reads:

- `X-Role` – role of the caller (recruiter, candidate, admin, etc.).  
- `X-User-Id` – identifier of the authenticated user.  

These headers are used to:

- restrict access to certain endpoints,  
- filter datasets,  
- adjust behaviour depending on the caller’s role.  

Cognito groups can support more granular permissions if required.

---

## 7. Response Model

Responses follow the standard API Gateway Lambda proxy format:

    {
      "statusCode": 200,
      "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      "body": "{ ... JSON string ... }"
    }

### 7.1 Success Responses

A successful request returns either:

- a single entity, or  
- a list of entities.  

### 7.2 Error Responses

Errors follow a structured format:

    {
      "error": "error_code",
      "message": "Human readable description"
    }

Standard error codes include:

- 400 – invalid input  
- 404 – entity not found  
- 409 – business conflict  
- 500 – internal error  

---

## 8. Process Workflow Summary

The `process-lambda` implements all workflow logic related to selection processes.

### 8.1 Workflow Capabilities

- Create processes linked to offers.  
- Retrieve processes.  
- Update processes (notes, status, closing).  
- Generate compatible candidates.  

### 8.2 Candidate Generation Logic

When calling:

    POST /processes/{processId}/candidates:generate

the Lambda:

1. Loads the process and the associated offer.  
2. Retrieves candidate records.  
3. Applies matching rules: role, similar roles, experience and other defined criteria.  
4. Produces a list of matching candidates.  
5. Stores this list inside the process item in DynamoDB.  

This keeps all process-related logic isolated in a dedicated Lambda, maintaining a clean and modular backend architecture.
