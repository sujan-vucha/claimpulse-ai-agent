# ClaimPulse: Autonomous AI Agentic Adjudication Suite 🛡️⚡

<div align="center">

### Enterprise AI Platform for Autonomous Insurance Claim Verification & Fraud Detection

*Powered by Google Gemini Multimodal Vision • FastAPI • React • MongoDB*

</div>

---

## 🌟 Executive Overview

Traditional insurance claim processing often involves manual inspection, delayed approvals, and subjective fraud assessment. **ClaimPulse** automates this workflow through an AI-powered agentic pipeline that analyzes claim images, validates evidence quality, evaluates user risk history, and generates an explainable adjudication decision in seconds.

The platform combines **multimodal computer vision**, **deterministic rule engines**, and **risk heuristics** to deliver instant, transparent, and audit-ready claim decisions.

---

# 📸 Platform Preview

## 🔐 Intelligent Login Portal

<p align="center">
  <img src="assets/login.png" alt="Login Portal" width="900"/>
</p>

Secure authentication with separate workspaces for:

* Policyholders
* Claims Adjusters
* JWT Authentication
* Role-Based Access Control (RBAC)

---

## 📝 Policyholder Claim Intake

<p align="center">
  <img src="assets/claiming.png" alt="Claim Submission" width="900"/>
</p>

Policyholders can:

* Select claim category
* Upload damage images
* Describe the incident
* Submit claims instantly
* Receive AI-generated decisions in real time

---

## 📊 Claims Adjuster Dashboard

<p align="center">
  <img src="assets/dashboard.png" alt="Dashboard" width="900"/>
</p>

The enterprise dashboard provides:

* Live claim monitoring
* Verdict filtering
* Search functionality
* Batch processing
* AI reasoning
* Fraud indicators

---

## 📄 Previous Claims

<p align="center">
  <img src="assets/previous_claims.png" alt="Previous Claims" width="900"/>
</p>

Policyholders can:

* Track submitted claims
* View adjudication history
* Download claim reports
* Monitor decision status

---

# 🚨 Example Case — Fraudulent Claim

<p align="center">
  <img src="assets/example1.png" alt="Contradicted Claim" width="850"/>
</p>

### User Claim

> "My vehicle suffered severe front bumper damage after a parking lot collision."

### AI Analysis

The multimodal vision agent observes:

* No structural deformation
* Only superficial dirt/wear
* Claimed component mismatch

### Verdict

```text
CONTRADICTED
```

Reason:

The uploaded image does not support the reported damage.

---

# ✅ Example Case — Genuine Claim

<p align="center">
  <img src="assets/trueClaiming.png" alt="Supported Claim" width="850"/>
</p>

### User Claim

> "Passenger side window was shattered due to vandalism."

### AI Analysis

The AI verifies:

* Visible shattered glass
* Correct vehicle component
* Damage severity consistent with user statement

### Verdict

```text
SUPPORTED
```

Evidence quality passes all validation checks.

---

# 🧠 Agentic Workflow

```
                     Policyholder Submission
                     (Image + Description)
                               │
                               ▼
                  FastAPI REST Gateway
                               │
 ┌─────────────────────────────┼──────────────────────────────┐
 │                             │                              │
 ▼                             ▼                              ▼
Vision Agent            Evidence Engine              Risk Engine
(Google Gemini)         Rule Validation            User History
 │                             │                              │
 └──────────────┬──────────────┴──────────────┬───────────────┘
                ▼
        Decision Synthesis Engine
                │
                ▼
      Explainable AI Adjudication
                │
                ▼
 Supported • Contradicted • Insufficient Information
```

---

# 🚀 Key Features

* AI-powered image damage analysis
* Google Gemini multimodal vision
* Explainable AI reasoning
* Fraud detection
* Evidence validation
* Deterministic decision engine
* Risk profiling
* JWT authentication
* Role-Based Access Control
* Batch CSV processing
* MongoDB persistence
* Local JSON fallback
* Responsive React dashboard
* REST APIs
* Swagger documentation

---

# 🛠️ Technology Stack

| Layer          | Technologies                  |
| -------------- | ----------------------------- |
| AI             | Google Gemini 3.1 Flash Lite  |
| Backend        | FastAPI, Python 3.11, Uvicorn |
| Frontend       | React 18, Vite, Axios         |
| Database       | MongoDB, PyMongo              |
| Authentication | JWT, Passlib Bcrypt           |
| Storage        | MongoDB + Local JSON Backup   |
| API Docs       | Swagger                       |
| Styling        | Vanilla CSS, Glassmorphism    |

---

# 📂 Project Structure

```text
claimpulse-ai-agent/

├── api/
├── frontend/
├── assets/
│   ├── login.png
│   ├── claiming.png
│   ├── dashboard.png
│   ├── previous_claims.png
│   ├── example1.png
│   └── trueClaiming.png
├── sample_claims.csv
├── requirements.txt
├── README.md
└── .env.example
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/sujan-vucha/claimpulse-ai-agent.git

cd claimpulse-ai-agent
```

---

## Configure Environment

Copy the example environment file.

```bash
cp .env.example .env
```

Update it with your credentials.

```env
GEMINI_API_KEY=YOUR_API_KEY

JWT_SECRET=YOUR_SECRET

MONGODB_URI=mongodb://localhost:27017/claimpulse
```

---

# ▶️ Run Backend

Install dependencies.

```bash
pip install -r requirements.txt
```

Launch FastAPI.

```bash
python -m uvicorn api.main:app --reload
```

Backend

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

# ▶️ Run Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:5173
```

---

# 🔑 Demo Credentials

| Role            | Email                                                           | Password |
| --------------- | --------------------------------------------------------------- | -------- |
| Claims Adjuster | [adjuster@claimpulse.io](mailto:adjuster@claimpulse.io)         | admin    |
| Policyholder    | [policyholder@claimpulse.io](mailto:policyholder@claimpulse.io) | admin    |

You may also register a new account using the Create Account option.

---

# 📦 Batch Processing

Claims Adjusters can upload:

* sample_claims.csv
* claims.csv

The system automatically:

* Executes claims sequentially
* Respects API rate limits
* Stores results
* Generates AI verdicts
* Exports processed CSV files

---

# 🔍 Decision Pipeline

Each claim undergoes the following stages:

1. Image Analysis using Gemini Vision
2. Evidence Quality Validation
3. Damage Localization
4. Severity Estimation
5. User Risk Evaluation
6. Decision Synthesis
7. Explainable Verdict Generation
8. Persistent Storage

---

# 📜 API Endpoints

| Method | Endpoint  | Description          |
| ------ | --------- | -------------------- |
| POST   | /login    | User Login           |
| POST   | /register | Create Account       |
| POST   | /claim    | Submit Claim         |
| GET    | /claims   | View Claims          |
| GET    | /me       | User Profile         |
| POST   | /batch    | Batch CSV Processing |

---

# 💡 Future Improvements

* OCR document verification
* VIN validation
* Geolocation verification
* Video claim analysis
* LLM-powered fraud explanation
* Human-in-the-loop approval
* Email notifications
* Multi-language support
* Cloud deployment
* Analytics dashboard

---

# 📄 License

Developed for the **Google DeepMind × HackerRank Advanced Agentic Coding Hackathon (2026)**.

This project is intended for educational, research, and hackathon demonstration purposes.
