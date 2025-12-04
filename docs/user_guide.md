# User Guide – Recruiter Platform

This document describes how to use the Recruiter Platform from the perspective of each type of user: recruiter, administrator, candidate, and company.

---

## 1. Access and Authentication

The platform uses **Amazon Cognito** for login and session management.  
Each user logs in with their credentials and is taken to their corresponding dashboard.

User types:

- **Recruiter**
- **Administrator**
- **Candidate**
- **Company**

---

## 2. Permissions and Visibility

### Recruiter

This is the main operational profile of the platform (together with the administrator).

A recruiter can view and manage:

- all **roles**
- all **candidates**
- all **offers**
- all **processes**
- all **workflow alerts**

A recruiter can also:

- edit and validate data created by candidates and companies  
- delete records when required  
- generate compatible candidates for a process  
- close processes  

### Administrator

Has the same visibility and permissions as the recruiter.

### Candidate

A candidate can:

- create their own profile  
- view and edit **only their own data**

A candidate cannot access:

- other candidates  
- offers  
- roles  
- processes  

### Company

A company user can:

- create and view **their own job offers**

They cannot see:

- candidates  
- roles  
- processes  
- offers created by other companies  

---

## 3. Roles

The **Roles** section contains the catalogue of job roles used throughout the platform.

### Create Role

A recruiter or administrator can create a role by entering its name.

### Edit Role

The name of an existing role can be updated.

### Delete Role

Roles can be deleted when they are no longer needed.

---

## 4. Candidates

### How Candidates Are Created

A candidate can exist in the platform in two ways:

- by **self-registration**, when a candidate creates their own profile  
- by **a recruiter**, who manually creates a candidate record  

### Candidate Information

A candidate profile may include:

- personal data  
- associated role  
- location  
- experience  
- strengths  
- salary expectations  
- internal notes (visible only to recruiter/administrator)

### Editing and Deleting

- A candidate can only edit **their own profile**.  
- Recruiters and administrators can view and edit **any candidate**.  
- Recruiters and administrators can delete candidates when necessary.

---

## 5. Offers

### How Offers Are Created

An offer may be created by:

- a **company**  
- a **recruiter**

### Offer Information

An offer typically includes:

- company  
- contact person  
- associated role  
- modality  
- location  
- job description  
- internal notes (recruiter/admin only)

### Editing and Deleting Offers

- A company can only manage **its own offers**.  
- Recruiters and administrators can view, edit, and delete **all offers**.

---

## 6. Selection Processes

### Automatic Process Creation

Whenever a **new offer** is created, the platform automatically creates a **selection process** linked to that offer.  
Processes do not need to be created manually by the user.

### What a Process Contains

A process includes:

- the related offer  
- process status (OPEN / CLOSED)  
- internal notes  
- similar roles (optional)  
- the list of candidates generated as compatible with the offer  

### Generating Compatible Candidates

Inside a process, the recruiter can trigger **Generate Candidates**.

The platform will:

1. take the role of the offer  
2. apply similar roles if defined  
3. evaluate all existing candidates  
4. generate a list of compatible candidates  
5. store that list inside the process record  

### Managing and Closing a Process

A recruiter can:

- review and manage the list of candidates in the process  
- update internal notes  
- update the process status  
- close the process once the selection is complete  

---

## 7. Workflow (Alerts for Recruiters)

The **Workflow** section acts as a review area for the recruiter.

It displays items created directly by:

- candidate users (new self-registrations)  
- company users (new offers created by companies)

The recruiter must:

- review the newly created information  
- validate and approve it  
- correct it if needed  
- or delete it if it is not valid  

This section essentially functions as a "pending validation" inbox.

---

## 8. Settings

### 8.1 Language Selection

The platform includes a complete i18n system.  
Available languages:

- 🇬🇧 **English**  
- 🇩🇪 **German**  
- 🇫🇷 **French**  
- 🏴 **Gaelic**  
- 🇮🇹 **Italian**  
- 🇨🇭 **Romansh**  
- 🇪🇸 **Spanish**  
- 🇪🇺 **Basque (Euskera)**  
- 🇨🇦 **Catalan**  

The user may change the interface language from the **Settings** menu.

### 8.2 Logout

The user may log out from the Settings section, which ends the current session and returns to the login page.

---


