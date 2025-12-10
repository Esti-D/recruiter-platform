# Recruiter Platform – Serverless Architecture (AWS)

This project implements a complete recruitment management platform designed as a fully serverless solution using AWS services.

The platform includes:
- A React + Vite frontend deployed on S3 (and optionally CloudFront)
- A backend based on AWS Lambda + API Gateway
- Data storage in DynamoDB
- Authentication through Cognito
- Automatic creation of selection processes and workflow alerts

---

## 1. Features Overview

### Recruiter Features
- Manage candidates, offers, roles, and selection processes
- Review workflow alerts created by candidate/company users
- Generate compatible candidates for each selection process
- Close and document selection processes

### Candidate Features
- Create and manage their own profile
- Access only their own data

### Company Features
- Create and manage their own job offers
- Access only their own offers

### Administrator
- Same privileges as recruiter

---

## 2. Architecture Summary

### Frontend
- Built with React + Vite  
- Deployed as static assets on S3  
- Optional CloudFront distribution for global delivery  
- Internationalisation (i18n) with supported languages:
  - English
  - German
  - French
  - Gaelic (Irish)
  - Italian
  - Romansh
  - Spanish
  - Basque (Euskera)
  - Catalan

### Backend
Two independent AWS Lambda functions:
- recruiter-core-lambda → roles, offers, candidates, workflow  
- process-lambda → processes and candidate generation  

Delivered through API Gateway with a Cognito authorizer.

### Data Layer
DynamoDB tables:
- ROLES_TABLE  
- CANDIDATES_TABLE  
- OFFERS_TABLE  
- PROCESSES_TABLE  

---

## 3. Folder Structure

repository  
│  
├── frontend/  
│   └── React + Vite application  
│  
├── backend/  
│   ├── recruiter-core-lambda/  
│   └── process-lambda/  
│  
└── documentation/  
    ├── ARCHITECTURE.md  
    ├── BACKEND.md  
    ├── DATABASE.md  
    ├── FRONTEND.md  
    ├── USER_GUIDE.md  
    ├── DEPLOYMENT.md  
    └── INFRA.md  
---

## 4. Environment Variables

### Frontend
VITE_API_BASE_URL pointing to API Gateway.

### Backend (Lambda)
CANDIDATES_TABLE  
OFFERS_TABLE  
ROLES_TABLE  
PROCESSES_TABLE  

---

## 5. Deployment Summary

### Frontend
1. npm install  
2. npm run build  
3. Upload dist/ to S3  
4. (Optional) Invalidate CloudFront

### Backend
1. Zip Lambda code  
2. Upload to Lambda  
3. Publish new version  
4. Test endpoints through API Gateway  


---

## 6. Monitoring & Observability

The platform includes full monitoring powered by CloudWatch:

- Metrics: Lambda, DynamoDB, API Gateway  
- Alarms:
  - Lambda errors and duration  
  - API Gateway 5xx  
  - DynamoDB throttling  
- SNS email notifications  
- CloudWatch dashboard: `recruiter-platform-dashboard`

All monitoring resources are deployed automatically through Terraform (see **INFRA.md**).

---

## 7. Documentation

Full technical documentation can be found in:
- ARCHITECTURE.md  
- BACKEND.md  
- DATABASE.md  
- FRONTEND.md  
- USER_GUIDE.md  
- DEPLOYMENT.md
- INFRA.md  

---


## 8. Infrastructure Overview (Terraform)

The Recruiter Platform is deployed as a fully serverless architecture, and all AWS resources are provisioned via Terraform.

Terraform manages:

- **S3 + CloudFront** → static hosting  
- **API Gateway HTTP API** → backend entry point  
- **Lambda functions** → compute layer  
- **DynamoDB tables** → persistent storage  
- **Cognito** → authentication  
- **CloudWatch + SNS** → alarms, dashboard and notifications  

See **INFRA.md** for a complete breakdown of all Terraform modules, lifecycle, IAM roles and monitoring strategy.

---

## 9. About

Recruiter Platform – Serverless AWS Implementation  
Designed and implemented as an end-to-end cloud architecture project, following AWS best practices in scalability, cost efficiency, security and operational excellence.
