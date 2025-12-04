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
    └── DEPLOYMENT.md  

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
4. Test via API Gateway  

---

## 6. Documentation

Full technical documentation can be found in:
- ARCHITECTURE.md  
- BACKEND.md  
- DATABASE.md  
- FRONTEND.md  
- USER_GUIDE.md  
- DEPLOYMENT.md  

---

## 7. Author

Recruiter Platform – AWS Serverless Implementation  
Created as part of a complete end-to-end cloud architecture project.

