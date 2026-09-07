# GenAI Platform for Automated Content Transformation
### Secure Blockchain-Backed Source-Grounded Multimodal Transformation Engine
**Smart India Hackathon (SIH 2026)**  
**Problem Statement ID:** 26154 | **Theme:** Blockchain & Cybersecurity | **Category:** Software  
**Organization:** National Technical Research Organisation (NTRO)  
**Team Name:** Goated Tech  
**Team Members:** Shreya Das, Piyush Kumar, Shreya Mandal, Aditi Maity, Soham Maiti, Ankita Mandal  

---

## 🌟 Executive Summary
Organisations frequently need to transform raw, heterogeneous information—such as threat advisories, technical reports, intelligence briefs, news articles, video recordings, or policy whitepapers—into specialized, audience-tailored communication artefacts. Manual synthesis is slow, inconsistent, and highly vulnerable to human bias or misinterpretation. 

Our solution is a **defense-grade, AI-powered content transformation engine** built for the **National Technical Research Organisation (NTRO)**. It ingests multimodal source materials (Text, PDF, Images, Audio, Video transcripts) and transforms them concurrently into **7 distinct, audience-ready artefacts** (Structured Advisories, Executive Briefings, Video Production Packages, LinkedIn Posts, Twitter/X Threads, Infographic Blueprints, and Slide Decks). 

Crucially, under the theme of **Blockchain & Cybersecurity**, every generated output undergoes rigorous **Source-Grounded Factuality Validation (Lewis et al.)**, is cryptographically fingerprinted via **SHA-256**, and has its provenance immutably recorded onto a **Permissioned Blockchain Ledger (Proof-of-Authority)**. This eliminates hallucinations, prevents tampering, and guarantees an unbreakable chain of custody from raw intelligence to final broadcast.

---

## 🚀 Core Features & Innovation

1. **Multimodal Ingestion Engine:**
   - PDF & Document parsing via `PyMuPDF (fitz)`
   - Audio & Speech-to-Text via `OpenAI Whisper`
   - Video transcription and metadata scraping via `yt-dlp`
   - Web intelligence scraping via `newspaper3k`
   - OCR & Image fact extraction

2. **Source-Grounded RAG & Semantic Router:**
   - Mathematical claim alignment against source embeddings (Lewis et al. RAG framework).
   - Dynamic parameter routing: Target Audience, Tone, Language, Level of Detail, Communication Objective, and Content Style Presets.

3. **Multi-Agent Concurrent Generation (7 Artefacts):**
   - **Structured Security Advisory:** CERT-In / NTRO standard format, CVE attribution, CVSS 3.1 severity, IOCs, actionable mitigations, and NIST CSF 2.0 mapping.
   - **Executive Briefing (BLUF):** Bottom Line Up Front, strategic risk, resource allocation, and organizational impact.
   - **Multimodal Video Package:** Complete 60-second video script, scene-by-scene storyboard, visual direction cues, narration timing, and subtitles.
   - **LinkedIn Executive Post:** Thought leadership, key takeaways, hashtags, and engagement hooks.
   - **Twitter/X Intelligence Thread:** 5-part platform-optimized thread with hooks and technical IOC summaries.
   - **Infographic Blueprint:** Visual layout grid, data hierarchy, icon recommendations, and key metric callouts.
   - **Technical Presentation Slides:** 5 structured slides with titles, visual layouts, bullet points, and speaker notes.

4. **Blockchain Provenance & Cybersecurity Guardrails:**
   - **Off-Chain Confidential Storage:** Sensitive intelligence remains isolated off-chain to safeguard classified material.
   - **On-Chain SHA-256 Provenance Fingerprint:** Only cryptographic hashes, source hashes, operator IDs, timestamps, and Merkle tree roots are stored on-chain.
   - **Permissioned Proof-of-Authority (PoA) Ledger:** Consensus maintained across verified defense nodes (`NTRO-NODE-ALPHA`, `CERT-IN-NODE-01`, `GOATED-TECH-NODE-GATEWAY`).
   - **Interactive Live Tamper-Detection:** Instantly flags single-character modifications to any published artefact.
   - **Role-Based Access Control (RBAC):** Strict operational segregation between Operators, Analysts, Officers, and Auditors.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
|---|---|
| **Frontend UI** | React.js, TailwindCSS, Lucide Icons, Space Grotesk & Inter typography |
| **Backend API** | FastAPI (Python 3.11), Pydantic v2, Uvicorn (ASGI) |
| **Generative AI & LLM** | Google Gemini 2.5 Flash, OpenAI Whisper (Speech-to-Text) |
| **Ingestion Tooling** | PyMuPDF (`fitz`), `newspaper3k`, `yt-dlp`, `beautifulsoup4` |
| **Cryptography & Ledger** | SHA-256, Merkle Trees, Proof-of-Authority (PoA) Permissioned Ledger |
| **Cybersecurity Standards** | NIST CSF 2.0, NIST SP 800-53 Rev. 5, STIX 2.1 / TAXII, RBAC |
| **Containerization** | Docker, Docker-Compose |

---

## ⚙️ Installation & Setup Guide

### Option 1: Quick Run via Standalone UI (Instant Prototype)
The prototype features a completely self-contained, interactive single-page application (`index.html`) that runs in any modern browser without external dependencies.
```bash
# Clone the repository
git clone https://github.com/GoatedTech-SIH2026/ntro-genai-content-transformation.git
cd ntro-genai-content-transformation

# Open directly in your browser
open index.html
# Or start a simple local server:
python3 -m http.server 3000
```
Visit `http://localhost:3000` to interact with all tabs: Main Studio, Blockchain Ledger, Architecture Document, Demo Video, and Technical Presentation.

---

### Option 2: Full Stack Local Setup (FastAPI Backend + React Frontend)

#### Prerequisites:
- Python 3.11+
- Node.js 18+ and npm
- Docker & Docker Compose (optional)

#### 1. Backend Setup:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt

# Export your Gemini API Key
export GEMINI_API_KEY="your_api_key_here"

# Start FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be accessible at: `http://localhost:8000/docs`.

#### 2. Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```
Frontend will be running at: `http://localhost:3000`.

---

### Option 3: Docker Compose (One-Command Deployment)
```bash
docker-compose up --build
```
- Frontend UI: `http://localhost:3000`
- Backend REST API: `http://localhost:8000`
- API Swagger Docs: `http://localhost:8000/docs`

---

## 📡 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | System health check, validator node status, and block height |
| `POST` | `/api/transform` | Core pipeline: ingests source, extracts facts, routes to agents, validates, hashes, and mints on-chain |
| `GET` | `/api/blockchain/ledger` | Returns the entire chronological permissioned blockchain ledger |
| `POST` | `/api/blockchain/verify` | Verifies cryptographic integrity of an artefact against on-chain records |

---

## 👥 Team Details — Goated Tech (NTRO PS ID: 26154)
- **Shreya Das** (Team Lead)
- **Piyush Kumar** (AI Systems & Backend Architecture)
- **Shreya Mandal** (Blockchain & Cryptography Specialist)
- **Aditi Maity** (Full-Stack UI/UX Engineer)
- **Soham Maiti** (Cybersecurity & Threat Intelligence Analyst)
- **Ankita Mandal** (Data Pipeline & Multimodal Ingestion)

---
*Developed for Smart India Hackathon (SIH 2026) under the auspices of the National Technical Research Organisation (NTRO).*
