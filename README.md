# ClaimPulse: Autonomous AI Agentic Adjudication Suite 🛡️⚡

An enterprise-grade **AI Agentic Platform** engineered to autonomously evaluate, verify, and adjudicate insurance and asset damage claims in real time. 

By uniting **Multimodal Computer Vision (Google Gemini 3.1 Flash)** with deterministic evidentiary engines and user risk heuristics, **ClaimPulse** eliminates adjudication bottlenecks, detects fraudulent submissions with zero latency, and provides 100% audit-ready traceability.

---

## 🌟 Executive Overview

Traditional insurance claim processing suffers from multi-day bottlenecks, manual visual inspection errors, and subjective fraud assessments. **ClaimPulse** transforms this workflow into an autonomous, agentic verification pipeline:
1. **Visual Impact & Geometry Inspection**: Multimodal AI parses damage photographs to pinpoint affected components (e.g., windshields, bumpers, electronic screens) and grade physical damage severity.
2. **Evidentiary Standard Guardrails**: Automated checks ensure photographic evidence meets minimum clarity and structural thresholds before proceeding.
3. **Deterministic Verdict Synthesis**: By combining visual observations with policyholder history risk scores, the engine generates an instant, explainable verdict (`Supported`, `Contradicted`, or `Insufficient Information`).

---

## 🧠 System Architecture & Agentic Workflow

```
[ Policyholder Submission ] ──(Image & Stated Claim)──> [ FastAPI REST Gateway ]
                                                                │
         ┌──────────────────────────────────────────────────────┴──────────────────────────────────────────────────────┐
         ▼                                                      ▼                                                      ▼
 1️⃣ Vision Evaluation Layer                             2️⃣ Evidence Engine                                    3️⃣ Risk & Profile Engine
 (Gemini 3.1 Flash Vision)                             (Structural Compliance)                                (User History & Flagging)
         │                                                      │                                                      │
         └──────────────────────────────────────────────────────┬──────────────────────────────────────────────────────┘
                                                                ▼
                                                4️⃣ Deterministic Decision Synthesis
                                            (Verifiable Status & Audit Trail Synthesis)
                                                                │
                                                                ▼
                                             [ Adjudication Verdict & UI Audit Desk ]
```

---

## 📸 Enterprise Workspaces & Case Studies

### 🔐 1. Intelligent Portal & Multi-Role Access (`login.png`)
Features a minimalist, cinematic architectural interface built with custom color theory and frosted crystal glass aesthetics. Supports two distinct enterprise roles:
* **Policyholder Role**: Submit claims, upload photographic proof, and monitor real-time AI verdicts.
* **Claims Adjuster Role**: Enterprise overview of all claims across the platform, deep-dive inspection tools, batch CSV execution, and telemetry analytics.

---

### 📝 2. Policyholder Claim Intake Studio (`claiming.png`)
An intuitive workspace allowing users to select asset categories (Automobile, Electronics, Shipping Packages), detail incident transcripts, and attach photographic evidence. The system immediately initiates the agentic verification pipeline upon submission.

---

### 📊 3. Adjuster Adjudication Desk (`dashboard.png` & `previous_claims.png`)
* **Admin Overview**: Adjusters monitor real-time verdicts across all submitted claims with instant filtering by status (`Supported`, `Contradicted`), asset category, or keyword search.
* **Policyholder History**: Policyholders have a dedicated view (`previous_claims.png`) to track their personal historical submissions and download synthesis records.

---

### 🧪 Case Study: Fraud Detection vs. Genuine Verification

#### 🚨 Case A: Contradicted / False Claim (`example1.png`)
* **Policyholder Statement**: *Stated extensive structural front bumper crushing from a parking lot hit-and-run.*
* **Agentic Visual Observation**: The Vision AI inspects the uploaded photograph (`example1.png`) and identifies only superficial dirt/light wear, or structural mismatch against the stated component.
* **Synthesized Verdict**: **`CONTRADICTED`** (Flagged for Adjuster Review / Zero Severity). The system prevents fraudulent payout while detailing exact visual mismatches in the audit trail.

#### ✅ Case B: Supported / True Claim (`trueClaiming.png`)
* **Policyholder Statement**: *Stated shattered passenger door window caused by vandalism while parked.*
* **Agentic Visual Observation**: The Vision AI inspects `trueClaiming.png`, verifying visible glass fracturing and structural compromise on the exact claimed vehicle component (`door / window`).
* **Synthesized Verdict**: **`SUPPORTED`** (Evidence Standard Met / Medium-High Severity). Approved with full justification synthesized in `< 2.0 seconds`.

---

## 🛠️ Technology Stack

| Layer | Technologies & Tools |
| :--- | :--- |
| **Artificial Intelligence** | Google GenAI SDK (`gemini-3.1-flash-lite`), Multimodal Vision Prompt Engineering |
| **Backend API Gateway** | Python 3.11, FastAPI, Uvicorn, Pydantic v2, Asynchronous Request Throttling |
| **Storage & Persistence** | PyMongo Driver (MongoDB) with automatic offline fallback to Local JSON Persistence (`local_storage.json`) |
| **Authentication & Security** | JWT Bearer Token Authentication, `passlib` Bcrypt Cryptography, Role-Based Access Control (RBAC) |
| **Frontend Enterprise UI** | React 18, Vite, Vanilla CSS Design System (Glassmorphism & Lucide Icons), Axios Interceptors |

---

## 🚀 Quick Start & Installation

### Prerequisites
* Python 3.10+
* Node.js 18+
* Google Gemini API Key (`GEMINI_API_KEY`)

### 1. Repository Setup & Environment
Clone the repository and set up your environment variables:
```bash
git clone https://github.com/sujan-vucha/claimpulse-ai-agent.git
cd claimpulse-ai-agent

# Create a copy of the environment template
cp .env.example .env
```
Ensure your `.env` file contains your active API key:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
JWT_SECRET=supersecretjwtkey_enterprise_secure_2026
MONGODB_URI=mongodb://localhost:27017/claimpulse
```
*(Note: If MongoDB is offline or unavailable, ClaimPulse automatically falls back to secure local file storage).*

### 2. Launch the Backend API Server
Install Python dependencies and start the FastAPI uvicorn engine:
```bash
pip install -r requirements.txt
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
*API Swagger Documentation is available live at `http://localhost:8000/docs`.*

### 3. Launch the Frontend Enterprise Portal
Open a new terminal window, install React dependencies, and start Vite:
```bash
cd frontend
npm install
npm run dev
```
Navigate to **`http://localhost:5173`** in your browser.

---

## 🔑 Demo Access Credentials

To test the multi-role agentic workflows immediately, use the built-in enterprise test accounts or click **Create Account** to register a new profile:

| Account Role | Username / Email | Password | Permissions & Workspace |
| :--- | :--- | :--- | :--- |
| **Claims Adjuster** | `adjuster@claimpulse.io` | `admin` | Global Adjudication Desk, Audit Inspection, Batch CSV Runner, Analytics Hub |
| **Policyholder** | `policyholder@claimpulse.io` | `admin` | Claim Intake Studio, Personal Submission History (`My Recent Claims`) |

---

## 📦 Batch Execution Studio

For enterprise testing over competition datasets, log in as an **Adjuster** and navigate to the **Batch Runner** tab. Select `sample_claims.csv` or `claims.csv` to run sequential automated evaluations across all records with rate-limit compliance, and export verified results directly to CSV.

---

## 📄 License & Attribution
Engineered for the Google DeepMind & HackerRank Advanced Agentic Coding Hackathon (2026). All rights reserved.
