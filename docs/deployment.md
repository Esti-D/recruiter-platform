# Deployment – Recruiter Platform (AWS)

This document describes how the Recruiter Platform is deployed using AWS serverless services.  
The architecture is based on Amazon S3, CloudFront, Lambda, DynamoDB, API Gateway and Cognito.

## 1. Overview

The platform consists of two main components:

### Frontend  
A static web application built with React + Vite, deployed to an Amazon S3 bucket and optionally delivered through CloudFront.

### Backend  
A serverless API based on two AWS Lambda functions behind Amazon API Gateway:  
- recruiter-core-lambda: roles, candidates, offers, workflow  
- process-lambda: selection processes and candidate generation  

DynamoDB stores the application data and Cognito manages user authentication.

---

## 2. Frontend Deployment

### Build  
The production build is generated using npm install and npm run build.  
The output is placed in the dist directory.

### Deployment to S3  
1. Create or select an S3 bucket with static website hosting enabled.  
2. Upload all files from the dist folder.  
3. Configure:  
   - Index document: index.html  
   - Error document: index.html  

### Optional CloudFront Distribution  
To improve global performance and enable HTTPS:  
- Create a CloudFront distribution with the S3 bucket as the origin.  
- Set the default root object to index.html.  
- Configure error responses to fallback to index.html.  
- Attach an ACM SSL certificate.

---

## 3. Backend Deployment

The backend is composed of two independent Lambda functions.

### recruiter-core-lambda  
Handles: roles, candidates, offers, workflow.  
Environment variables:  
CANDIDATES_TABLE  
OFFERS_TABLE  
ROLES_TABLE  
PROCESSES_TABLE  

### process-lambda  
Handles: process creation, process updates, candidate generation.  
Deployment flow is identical to recruiter-core-lambda.

---

## 4. API Gateway Configuration

### Routing  
- /roles → recruiter-core-lambda  
- /candidates → recruiter-core-lambda  
- /offers → recruiter-core-lambda  
- /workflow → recruiter-core-lambda  
- /processes → process-lambda  

### CORS  
Access-Control-Allow-Origin: *  
Access-Control-Allow-Headers: Authorization, X-Role, X-User-Id, Content-Type  
Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS  

### Cognito Authorizer  
API Gateway validates JWT tokens using a Cognito User Pool Authorizer.  
Requests must include: Authorization: Bearer <token>

---

## 5. DynamoDB Configuration

Required tables:  
ROLES_TABLE  
CANDIDATES_TABLE  
OFFERS_TABLE  
PROCESSES_TABLE  

Each table uses a simple partition key.  
Recommended mode: On-demand.

---

## 6. Cognito Configuration

Cognito includes:  
User Pool  
App Client  
Optional Hosted UI  
User groups: recruiter, admin, candidate, company  

The frontend uses Cognito tokens for API calls.

---

## 7. Environment Variables

### Frontend  
VITE_API_BASE_URL pointing to the API Gateway URL.

### Backend  
CANDIDATES_TABLE  
OFFERS_TABLE  
ROLES_TABLE  
PROCESSES_TABLE  

---

## 8. Updating Deployments

### Updating the Frontend  
1. Run the build to regenerate the dist folder.  
2. Upload new files to S3.  
3. If CloudFront is used, invalidate cache.

### Updating the Backend  
1. Upload the updated Lambda ZIP package.  
2. Publish a new version.  
3. Test the endpoints via API Gateway.

---

## 9. Monitoring and Logging

Monitoring is done via CloudWatch:  
- Lambda logs  
- API Gateway logs  
- DynamoDB metrics  
- Cognito metrics  

Recommended alarms:  
- Lambda errors  
- API Gateway 5xx  
- High latency  
- DynamoDB throttling  

---



