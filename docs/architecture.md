# Architecture – Recruiter Platform (S3 + Lambda version)

This document describes the serverless architecture of the *Recruiter Platform* application, built using AWS managed services: **S3, CloudFront, API Gateway, Lambda, DynamoDB, and Cognito**.

---

## 1. Solution Objective

The platform allows a recruiter to manage:

- **Candidates**
- **Job offers**
- **Selection processes**
- **A catalogue of roles**

The main objective of this solution is to define an efficient architecture for scenarios where the goal is:

- to use a **100% serverless architecture**, with no servers to maintain;
- to minimise cost and simplify scalability.

---

## 2. High-Level Overview

At a high level, the architecture consists of:

- A **static frontend** built with React + Vite, hosted in **Amazon S3** and optionally distributed via **Amazon CloudFront**.
- A **REST API** exposed using **Amazon API Gateway**.
- **Business logic** implemented in **AWS Lambda**.
- **Data persistence** in **Amazon DynamoDB**, with four main tables: `CANDIDATE`, `OFFER`, `PROCESS`, and `ROLE`.
- **Authentication and authorisation** managed with **Amazon Cognito**.

---

## 3. Main Components

### 3.1 Frontend (S3 + CloudFront)

- Built with **React + Vite**.
- The production build is deployed to an **S3 bucket** configured for static website hosting.
- Optionally served through **Amazon CloudFront** to improve latency and caching.
- The frontend communicates with the backend through an environment variable:
  - `VITE_API_BASE_URL` → public API Gateway endpoint.

### 3.2 Amazon API Gateway

- Exposes the application as a **REST API**.
- Routes are mapped to Lambda functions or to a single routing Lambda.
- Typical endpoints:
  - `/roles`
  - `/candidates`
  - `/offers`
  - `/process`
- Supports:
  - Basic input validation
  - Throttling
  - CORS configuration for the frontend domain

### 3.3 AWS Lambda (Backend)

- Implements all backend logic:
  - CRUD operations for roles, candidates, offers, and processes
  - Filtering and search
  - Automatic candidate selection for processes
- Developed in **Python**, using `boto3` for DynamoDB integration.
- Standard flow:
  - Lambda receives an API Gateway event
  - Determines route + HTTP method
  - Calls the corresponding service
  - Returns a normalised JSON response

### 3.4 DynamoDB (NoSQL Database)

Four main tables:

- `ROLE`
- `CANDIDATE`
- `OFFER`
- `PROCESS`

Each table uses a simple partition key (`roleId`, `candidateId`, etc.).  
Field details are documented separately in `DATABASE.md`.

Why DynamoDB:

- Fully managed serverless database
- No operational overhead
- Fits key-value and simple filtering requirements

### 3.5 Amazon Cognito (Authentication & Authorisation)

- Manages user login and identity.
- Issues **JWT tokens** (ID, access, refresh).
- Supports user groups such as:
  - `admin`
  - `recruiter`
  - `candidate`
- API Gateway uses a **Cognito Authorizer** to validate JWT tokens before invoking Lambda.

### 3.6 Observability (CloudWatch)

- Lambda logs are stored in **Amazon CloudWatch Logs**.
- Useful for:
  - Debugging during development
  - Basic monitoring in production

---

## 4. Data Model (Summary)

The application handles four main entities:

- **ROLE**: role catalogue
- **CANDIDATE**: candidate profiles with personal details, experience, notes, status, etc.
- **OFFER**: job offers including company, contact person, role, modality, location, description
- **PROCESS**: selection processes linked to an offer, with status, notes, and candidate lists

> Full field descriptions are available in `docs/DATABASE.md`.

---

## 5. Core Flows

### 5.1 Authentication Flow

1. User accesses the frontend (S3/CloudFront).
2. Authenticates via Cognito (Hosted UI or embedded form).
3. Cognito returns JWT tokens.
4. The frontend sends API requests with `Authorization: Bearer <token>`.
5. API Gateway validates the token before invoking Lambda.

### 5.2 CRUD Operations

1. User performs an action in the frontend (e.g., create an offer).
2. The frontend calls the corresponding API endpoint.
3. API Gateway triggers the appropriate Lambda function.
4. Lambda processes the request and interacts with DynamoDB.
5. Lambda returns the result through API Gateway.

### 5.3 Selection Process Workflow

1. Recruiter creates a job offer.
2. A process is created and linked to that offer.
3. A Lambda function can generate suggested candidates.
4. The process stores the list and current status (OPEN/CLOSED).
5. Recruiter updates notes and status as the process progresses.

---

## 6. Design Decisions

- **Serverless-first approach**: no servers, automatic scaling.
- **Loose coupling** between frontend and backend through REST API.
- **NoSQL data model** to allow flexible evolution of fields.
- **Managed authentication** instead of custom auth logic.
- **Pay-per-use cost model** ideal for variable workloads.

---

## 7. Limitations and Future Improvements

Possible enhancements for future iterations:

- Add **secondary indexes** (GSI/LSI) to DynamoDB for faster filtering.
- Split the backend into multiple smaller Lambda functions if desired.
- Add load tests and additional CloudWatch metrics.
- Implement **CI/CD pipelines** (GitHub Actions).
- Add CloudWatch alarms for error rates or high latency.

---
