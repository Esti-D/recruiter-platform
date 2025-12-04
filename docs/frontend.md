# Frontend – React + Vite + AWS S3

This document describes the frontend architecture of the Recruiter Platform.  
The frontend is implemented in **React + Vite**, communicates with a serverless backend on AWS, and is deployed as a static website on **Amazon S3** (optionally using CloudFront).

---

## 1. Overview

The frontend provides the user-facing interface for:

- managing candidates  
- managing offers  
- managing roles  
- managing selection processes  
- viewing workflow-oriented lists (candidates and offers)

The application is built with:

- **React 18**  
- **Vite** (development server and build tool)  
- **JavaScript/TypeScript**  
- **Material UI** components  
- custom hooks and services to call the backend API  

---

## 2. Project Structure

A simplified project layout is:

    frontend/
      src/
        components/
        pages/
        domain/
        api/
        config/
        hooks/
        styles/
        main.jsx
        App.jsx
      public/
      index.html
      vite.config.js

Key directories:

- `domain/` – domain models (Candidate, Offer, Role, Process)  
- `api/` – generic API helpers and domain-specific modules  
- `components/` – reusable UI components  
- `pages/` – main screens  
- `config/` – environment configuration (API URL, Cognito config, etc.)  

---

## 3. API Integration

The frontend communicates with the backend using a centralised API helper (based on `fetch` or similar).

### 3.1 Base URL

Configured via Vite environment variables:

    VITE_API_BASE_URL=<api-gateway-url>

Used in the API helper as:

    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

### 3.2 Auth Headers

After logging in through Cognito, the JWT token is sent on every request:

    Authorization: Bearer <token>

Additional headers:

    X-Role: <role>
    X-User-Id: <cognito_user_id>

These headers allow the backend to:

- determine permissions  
- filter results  
- adapt workflow behaviour  

### 3.3 API Modules

Typical modules:

- `api/candidates` – list, create, update, delete, workflow filters  
- `api/offers` – list, create, update, delete  
- `api/roles` – list, create, update, delete, reassign  
- `api/processes` – list, create, update, generate candidates  

Each module exposes small functions (for example: `listCandidates`, `createOffer`, `generateCandidates(processId)`), keeping UI components simple.

---

## 4. State Management

The app mainly uses:

- local React state (hooks)  
- simple context where global data is needed  
- derived state for filtering and sorting  

A global state library (Redux, Zustand, etc.) is not required for this version.

---

## 5. Routing

Routing is handled with React Router (or an equivalent lightweight setup).

Example routes:

- `/candidates`  
- `/candidates/:id`  
- `/offers`  
- `/offers/:id`  
- `/roles`  
- `/processes`  
- `/processes/:id`  
- `/workflow/candidates`  
- `/workflow/offers`  

Each route renders a page component that:

- loads data from the API  
- displays lists and forms  
- handles CRUD operations via the API modules  

---

## 6. Deployment

### 6.1 Build

To produce a production build:

    npm install
    npm run build

This generates the `dist/` folder containing:

- `index.html`  
- bundled JS/CSS assets  

### 6.2 Deployment to S3

Steps:

1. Create or use an S3 bucket configured for static website hosting.  
2. Upload the contents of `dist/` to the bucket.  
3. Configure:
   - index document: `index.html`  
   - error document: `index.html` (SPA fallback)  

The frontend then becomes accessible via the S3 website endpoint or through CloudFront.

### 6.3 Optional CloudFront CDN

Optionally, a CloudFront distribution can be added in front of the S3 bucket to:

- improve latency  
- add caching  
- serve via HTTPS with an ACM certificate  

---

## 7. Error Handling

The frontend includes:

- basic form validation  
- centralised API error handling in the API helper  
- user-facing messages for:
  - authentication issues  
  - validation errors  
  - network/backend failures  

---

## 8. Future Improvements

Potential future work:

- loading skeletons and better UX for slow requests  
- stronger form handling (for example, React Hook Form)  
- automated UI tests  
- automated deploy + CloudFront invalidation pipeline  

---