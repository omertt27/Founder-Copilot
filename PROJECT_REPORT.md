# 📋 FOUNDER COPILOT — FULL SYSTEM REPORT
### Amazon Nova AI Hackathon — Comprehensive Build & Architecture Report
**Date:** March 7, 2026  
**Project:** Founder Copilot — AI-Powered Startup Helper Agent  
**Stack:** Amazon Nova AI (Bedrock) + FastAPI + React/Vite  
**Version:** 1.0.0

---

## 1. PROJECT OVERVIEW

**Founder Copilot** is a production-ready full-stack web application that helps startup founders turn raw ideas into actionable plans using Amazon Nova AI. The app provides four core AI-powered features, plus an intelligent auto-detect agent and real-time streaming — each driven by carefully optimized prompts targeting Amazon Nova's **Premier, Pro, Lite, and Micro** models through Amazon Bedrock.

**Hackathon Goal:** Demonstrate the power of Amazon Nova AI models for real-world startup tooling — from ideation to investor pitch — with production-grade architecture, security, and UX.

---

## 2. SYSTEM ARCHITECTURE

### 2.1 High-Level Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     FRONTEND (React 18 / Vite 6)                 │
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ Startup  │ │  Tech    │ │  GitHub  │ │  Pitch   │            │
│  │  Plan    │ │  Arch    │ │  Issues  │ │  Deck    │            │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘            │
│       └─────────────┼───────────┼─────────────┘                  │
│                     ▼           ▼                                 │
│  ┌─────────────────────────────────────────────────┐             │
│  │        API Service (api.js)                      │             │
│  │   • REST calls with error handling               │             │
│  │   • SSE streaming support                        │             │
│  │   • 422/429 user-friendly error parsing          │             │
│  └─────────────────────┬───────────────────────────┘             │
│                        │                                          │
│  ┌─────────────────────────────────────────────────┐             │
│  │   localStorage: History Persistence (10 items)   │             │
│  └──────────────────────────────────────────────────┘             │
└────────────────────────┼─────────────────────────────────────────┘
                         │ HTTP/SSE (Vite proxy :5173 → :8000)
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI / Python 3.11+)                │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │  Rate Limiter (slowapi) — 10 requests/minute per IP      │     │
│  └──────────────────────┬───────────────────────────────────┘     │
│                         ▼                                         │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │                   routes.py (6 endpoints)                 │     │
│  │                                                           │     │
│  │  POST /api/generate/startup-plan                          │     │
│  │  POST /api/generate/tech-architecture                     │     │
│  │  POST /api/generate/github-issues                         │     │
│  │  POST /api/generate/pitch-deck                            │     │
│  │  POST /api/generate/auto      (multi-model agent)         │     │
│  │  POST /api/generate/stream/{feature}   (SSE)              │     │
│  │                                                           │     │
│  │  ┌──────────────────────────────────────────────┐         │     │
│  │  │ _invoke_async() — runs boto3 in thread pool  │         │     │
│  │  │ (prevents blocking the async event loop)      │         │     │
│  │  └──────────────────────────────────────────────┘         │     │
│  └──────────────────────┬───────────────────────────────────┘     │
│                         ▼                                         │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │             prompts.py (5 prompt templates)               │     │
│  │   • System prompt (shared)                                │     │
│  │   • Startup plan / Tech arch / GitHub issues / Pitch deck │     │
│  │   • Agent coordinator (intent classification)             │     │
│  └──────────────────────┬───────────────────────────────────┘     │
│                         ▼                                         │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │           nova_client.py (Bedrock Client)                 │     │
│  │                                                           │     │
│  │   _build_body()          → shared request builder         │     │
│  │   invoke()               → sync call, returns (text, tok) │     │
│  │   invoke_streaming()     → yields text chunks via SSE     │     │
│  │                                                           │     │
│  │   • Adaptive retry (3 attempts)                           │     │
│  │   • Token usage extraction from invocation metrics        │     │
│  └──────────────────────┬───────────────────────────────────┘     │
└──────────────────────────┼────────────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                      AMAZON BEDROCK                               │
│                                                                   │
│  ┌─────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │Nova Premier │ │ Nova Pro │ │ Nova Lite│ │Nova Micro│         │
│  │(most        │ │ (high    │ │(balanced)│ │ (fast    │         │
│  │ powerful)   │ │  quality)│ │          │ │  routing)│         │
│  └─────────────┘ └──────────┘ └──────────┘ └──────────┘         │
│                                                                   │
│  Region: us-east-1  •  API: messages-v1  •  Serverless            │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Request Flow (Example: Startup Plan)

```
User types idea → clicks "Generate"
        │
        ▼
InputPanel.jsx → onGenerate({ input, model: "premier" })
        │
        ▼
App.jsx → generateStartupPlan(input, "premier")
        │
        ▼
api.js → POST /api/generate/startup-plan { idea, model }
        │
        ▼ (Vite proxy → localhost:8000)
        │
routes.py → rate limit check (10/min)
        │
        ▼
_invoke_async() → thread pool executor
        │
        ▼
nova_client.invoke() → _build_body() + boto3.invoke_model()
        │
        ▼
Amazon Bedrock → Nova Premier (amazon.nova-premier-v1:0)
        │
        ▼
Response ← (text, tokens_used)
        │
        ▼
GenerationResponse { feature, content, model_used, tokens_used }
        │
        ▼
OutputPanel.jsx → ReactMarkdown render + copy/download
        │
        ▼
History ← saved to localStorage
```

### 2.3 Auto-Detect Agent Flow (Multi-Model Pipeline)

```
User: "Help me build an architecture for a SaaS tool"
        │
        ▼
 ┌──────────────────────────────────┐
 │  Step 1: Intent Classification   │
 │  Model: Nova Micro (fastest)     │
 │  Temp: 0.1 / Max tokens: 50     │
 │  Output: "tech_architecture"     │
 └──────────────────┬───────────────┘
                    ▼
 ┌──────────────────────────────────┐
 │  Step 2: Full Generation         │
 │  Model: User's choice (Premier)  │
 │  Temp: 0.3 / Max tokens: 4096   │
 │  Uses TECH_ARCHITECTURE_PROMPT   │
 └──────────────────────────────────┘
```

---

## 3. COMPLETE FILE INVENTORY

### 3.1 Backend (Python / FastAPI)

| File | Lines | Purpose |
|------|-------|---------|
| `backend/app/main.py` | 79 | FastAPI entry point, CORS, rate limiter setup, health checks |
| `backend/app/config.py` | 46 | Environment loader, AWS credentials, 4 Nova model IDs, model map |
| `backend/app/nova_client.py` | 129 | Bedrock client — `_build_body()`, `invoke()` (returns text + tokens), `invoke_streaming()` |
| `backend/app/prompts.py` | 317 | 5 optimized prompt templates for all features + agent coordinator |
| `backend/app/models.py` | 97 | 8 Pydantic schemas (4 requests, 3 responses, 2 enums) |
| `backend/app/routes.py` | 321 | 6 API endpoints with rate limiting, async thread offloading, token tracking |
| `backend/app/__init__.py` | 3 | Package initializer |
| `backend/run.py` | 13 | Uvicorn server runner with hot-reload |
| `backend/requirements.txt` | 8 | Python dependencies |
| `backend/.env` | 20 | Environment configuration (gitignored) |

**Total backend:** ~1,033 lines across 10 files

### 3.2 Frontend (React / Vite)

| File | Lines | Purpose |
|------|-------|---------|
| `frontend/src/main.jsx` | ~10 | React DOM entry point |
| `frontend/src/App.jsx` | 174 | Main app — state management, feature routing, localStorage history |
| `frontend/src/App.css` | 95 | Hero section, error banner, footer styles |
| `frontend/src/index.css` | 270 | Global design system — colors, typography, markdown, animations |
| `frontend/src/components/Header.jsx` | 29 | Navigation bar with brand logo + hackathon badge |
| `frontend/src/components/Header.css` | ~50 | Header styles |
| `frontend/src/components/FeatureCards.jsx` | 77 | 4 feature cards with Framer Motion animations |
| `frontend/src/components/FeatureCards.css` | ~80 | Card grid, selection states, color identities |
| `frontend/src/components/InputPanel.jsx` | 135 | Textarea, model selector (4 models), extra fields for GitHub Issues |
| `frontend/src/components/InputPanel.css` | 190 | Input styles, model buttons, responsive layout |
| `frontend/src/components/OutputPanel.jsx` | 84 | Markdown renderer, copy-to-clipboard, download, token display |
| `frontend/src/components/OutputPanel.css` | ~80 | Output panel styles |
| `frontend/src/components/LoadingSkeleton.jsx` | 45 | Animated skeleton with rotating AI status messages |
| `frontend/src/components/LoadingSkeleton.css` | ~60 | Skeleton animation styles |
| `frontend/src/components/History.jsx` | 81 | Persistent history list with feature icons + preview |
| `frontend/src/components/History.css` | ~60 | History panel styles |
| `frontend/src/services/api.js` | 144 | API client — 6 functions, SSE streaming, 422/429 error handling |
| `frontend/vite.config.js` | 19 | Dev server, proxy `/api` + `/health` to backend |
| `frontend/index.html` | ~20 | HTML shell with Google Fonts |
| `frontend/package.json` | 25 | NPM dependencies + scripts |
| `frontend/public/rocket.svg` | ~5 | Favicon |

**Total frontend:** ~1,700+ lines across 21 files

### 3.3 Project Root

| File | Lines | Purpose |
|------|-------|---------|
| `README.md` | 177 | Full documentation with setup guide, API reference, demos |
| `PROJECT_REPORT.md` | This file | Comprehensive system report |

---

## 4. FEATURES IMPLEMENTED

### Feature 1: 💡 Startup Plan Generator
| Property | Value |
|----------|-------|
| **Endpoint** | `POST /api/generate/startup-plan` |
| **Input** | Startup idea (free text, min 10 chars) |
| **Output** | 6 sections — Product Description, Target Users, MVP Features, 6-Month Roadmap, Success Metrics, Potential Challenges |
| **Temperature** | 0.3 (focused/structured) |
| **Default Model** | Nova Premier |

### Feature 2: 🏗️ Technical Architecture Generator
| Property | Value |
|----------|-------|
| **Endpoint** | `POST /api/generate/tech-architecture` |
| **Input** | Product description (min 10 chars) |
| **Output** | 6 sections — Tech Stack (with reasoning), System Architecture, Database Schema, API Endpoints, Security, Scalability |
| **Temperature** | 0.3 (precise/technical) |
| **Default Model** | Nova Premier |

### Feature 3: 📋 GitHub Issues Generator
| Property | Value |
|----------|-------|
| **Endpoint** | `POST /api/generate/github-issues` |
| **Input** | Product name + description + tech stack |
| **Output** | 15–20 prioritized issues with titles, priority (High/Med/Low), estimates, acceptance criteria, labels, technical notes |
| **Temperature** | 0.3 (structured) |
| **Default Model** | Nova Premier |

### Feature 4: 🎤 Pitch Deck Generator
| Property | Value |
|----------|-------|
| **Endpoint** | `POST /api/generate/pitch-deck` |
| **Input** | Startup idea + optional description |
| **Output** | 12-slide investor-ready deck — Cover, Problem, Solution, How It Works, Market, Business Model, Traction, Competition, GTM, Team, Financials, The Ask |
| **Temperature** | 0.7 (more creative) |
| **Default Model** | Nova Premier |

### Feature 5: 🤖 Smart Auto-Detect (Agent Coordinator)
| Property | Value |
|----------|-------|
| **Endpoint** | `POST /api/generate/auto` |
| **Step 1** | Nova Micro classifies intent (temp 0.1, max 50 tokens) |
| **Step 2** | Routes to correct feature with user's chosen model |
| **Pipeline** | Two-step multi-model orchestration |

### Feature 6: 📡 Real-Time Streaming
| Property | Value |
|----------|-------|
| **Endpoint** | `POST /api/generate/stream/{feature}` |
| **Protocol** | Server-Sent Events (SSE) |
| **Supports** | All 4 features with per-feature temperature |

---

## 5. AMAZON NOVA AI INTEGRATION

### 5.1 Models Configured

| Model | Model ID | Use Case | Capabilities |
|-------|----------|----------|--------------|
| **Nova Premier** | `amazon.nova-premier-v1:0` | Default model — most powerful | Complex reasoning, code gen, multimodal (text/image/video), agents, RAG |
| **Nova Pro** | `amazon.nova-pro-v1:0` | High-quality generation | Code gen, reasoning, conversation, RAG, translation |
| **Nova Lite** | `amazon.nova-lite-v1:0` | Balanced speed/quality | Conversation, Q&A, text gen, multimodal |
| **Nova Micro** | `amazon.nova-micro-v1:0` | Intent detection (fastest) | Text-to-text, Q&A, conversation, math |

### 5.2 Bedrock Integration Details

| Aspect | Implementation |
|--------|---------------|
| **AWS SDK** | `boto3` → `bedrock-runtime` service |
| **Sync API** | `invoke_model()` — returns full response + token count |
| **Streaming API** | `invoke_model_with_response_stream()` — yields `contentBlockDelta` chunks |
| **Request Format** | Nova `messages-v1` schema with system + user messages |
| **Inference Config** | `temperature`, `max_new_tokens` (4096), `topP` (0.9) |
| **Retry Strategy** | Adaptive mode, 3 max attempts (botocore) |
| **Token Tracking** | Extracts `inputTokenCount` + `outputTokenCount` from `amazon-bedrock-invocationMetrics` |
| **Body Builder** | Shared `_build_body()` helper eliminates duplication between sync/streaming |

### 5.3 Prompt Engineering

| Prompt | Lines | Strategy |
|--------|-------|----------|
| **System Prompt** | 5 | Shared persona: "Founder Copilot" — actionable, structured, Markdown |
| **Startup Plan** | ~55 | Role: startup advisor. 6 named sections with bullet templates |
| **Tech Architecture** | ~55 | Role: senior architect. Stack reasoning + schema + endpoints |
| **GitHub Issues** | ~60 | Role: technical PM. 15–20 issues with priority/estimate/criteria |
| **Pitch Deck** | ~80 | Role: pitch consultant. 12 slides with visual suggestions |
| **Agent Coordinator** | ~15 | Classification-only. Returns exactly one of 5 enum values |
| **Total** | ~317 lines | All optimized for structured Markdown output |

---

## 6. SECURITY & PRODUCTION FEATURES

| Feature | Implementation |
|---------|----------------|
| **Rate Limiting** | `slowapi` — 10 requests/minute per IP on all generation endpoints |
| **CORS** | Configurable allowed origins via `CORS_ORIGINS` env variable |
| **Input Validation** | Pydantic schemas with `min_length` constraints on all text fields |
| **Error Handling** | Backend: try/catch → HTTP 500 with detail. Frontend: 422 field-level parsing, 429 rate-limit messages |
| **Async Safety** | `_invoke_async()` runs blocking boto3 calls in `run_in_executor` thread pool |
| **Credentials** | AWS keys in `.env` file (gitignored), never hardcoded |
| **Deployment Ready** | `mangum` adapter included for AWS Lambda/API Gateway deployment |

---

## 7. UI/UX DESIGN SYSTEM

### 7.1 Visual Design

| Aspect | Details |
|--------|---------|
| **Theme** | Dark mode with purple/pink accent gradient |
| **Background** | Deep navy `#0a0a0f` (primary), `#12121a` (secondary), `#1a1a2e` (cards) |
| **Accent** | Purple `#6c63ff` (primary), Pink `#ff6b9d` (secondary) |
| **Gradient** | `linear-gradient(135deg, #6c63ff, #ff6b9d)` |
| **Typography** | Inter (body), JetBrains Mono (code) via Google Fonts |
| **Border Radius** | 8px (sm), 12px (md), 16px (lg), 24px (xl) |

### 7.2 Feature Color System

| Feature | Color | Hex |
|---------|-------|-----|
| 💡 Startup Plan | Purple | `#6c63ff` |
| 🏗️ Tech Architecture | Cyan | `#00d2ff` |
| 📋 GitHub Issues | Green | `#4ade80` |
| 🎤 Pitch Deck | Pink | `#ff6b9d` |

### 7.3 UX Features

| Feature | Details |
|---------|---------|
| ✅ Feature cards | 4 interactive cards with Framer Motion stagger animations (whileHover, whileTap) |
| ✅ Model selector | 4-button toggle: Premier (Most powerful), Pro (Best quality), Lite (Balanced), Micro (Fastest) |
| ✅ Markdown rendering | Full support: headers, lists, tables, code blocks, checkboxes, blockquotes |
| ✅ Copy to clipboard | One-click with fallback for older browsers |
| ✅ Download as `.md` | Generates timestamped Markdown file |
| ✅ Token display | Shows total tokens used per generation in output header |
| ✅ Loading skeleton | Animated shimmer lines + rotating status messages ("🧠 Amazon Nova is thinking...") |
| ✅ Persistent history | Last 10 generations saved to `localStorage`, survives page refresh |
| ✅ Error handling | User-friendly messages for validation (422), rate limits (429), and server errors |
| ✅ Responsive | Mobile-first with breakpoint at 700px |
| ✅ Custom scrollbar | Styled for dark theme |
| ✅ Selection highlight | Purple tint on text selection |

---

## 8. DEPENDENCIES

### 8.1 Backend (Python)

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | 0.115.6 | Web framework |
| `uvicorn[standard]` | 0.34.0 | ASGI server with hot-reload |
| `boto3` | 1.36.2 | AWS SDK for Bedrock access |
| `python-dotenv` | 1.0.1 | `.env` file loading |
| `pydantic` | 2.10.5 | Request/response validation |
| `mangum` | 0.19.0 | AWS Lambda adapter (deployment-ready) |
| `python-multipart` | 0.0.20 | Multipart form data support |
| `slowapi` | 0.1.9 | Rate limiting middleware |

### 8.2 Frontend (Node.js)

| Package | Version | Purpose |
|---------|---------|---------|
| `react` | 18.3.1 | UI framework |
| `react-dom` | 18.3.1 | DOM renderer |
| `react-markdown` | 9.0.1 | Markdown rendering for AI output |
| `react-icons` | 5.4.0 | Heroicons v2 icon library |
| `framer-motion` | 11.15.0 | Card animations (stagger, hover, tap) |
| `vite` | 6.0.7 | Build tool + dev server |
| `@vitejs/plugin-react` | 4.3.4 | React Fast Refresh plugin |

---

## 9. API REFERENCE

### 9.1 Health Endpoints

| Method | Endpoint | Rate Limited | Response |
|--------|----------|-------------|----------|
| `GET` | `/` | No | `{ status, service, version, nova_models }` |
| `GET` | `/health` | No | Same as above |
| `GET` | `/docs` | No | Swagger UI |
| `GET` | `/redoc` | No | ReDoc documentation |

### 9.2 Generation Endpoints

| Method | Endpoint | Rate Limited | Request Body | Response |
|--------|----------|-------------|-------------|----------|
| `POST` | `/api/generate/startup-plan` | 10/min | `{ idea, model }` | `{ feature, content, model_used, tokens_used }` |
| `POST` | `/api/generate/tech-architecture` | 10/min | `{ product_description, model }` | Same |
| `POST` | `/api/generate/github-issues` | 10/min | `{ product_name, product_description, tech_stack, model }` | Same |
| `POST` | `/api/generate/pitch-deck` | 10/min | `{ idea, product_description, model }` | Same |
| `POST` | `/api/generate/auto` | 10/min | `{ message, model, context }` | `{ detected_feature, content, model_used }` |
| `POST` | `/api/generate/stream/{feature}` | 10/min | `{ message, model }` | SSE: `data: {"text": "..."}` → `data: [DONE]` |

### 9.3 Model Values

Accepted values for the `model` field: `"premier"`, `"pro"`, `"lite"`, `"micro"`

---

## 10. DATA MODELS (Pydantic Schemas)

### Enums
```
NovaModel:    "premier" | "pro" | "lite" | "micro"
FeatureType:  "startup_plan" | "tech_architecture" | "github_issues" | "pitch_deck" | "auto_detect"
```

### Request Models
| Model | Fields |
|-------|--------|
| `StartupPlanRequest` | `idea` (str, min 10), `model` (default: premier) |
| `TechArchitectureRequest` | `product_description` (str, min 10), `model` |
| `GitHubIssuesRequest` | `product_name`, `product_description` (min 10), `tech_stack` (optional), `model` |
| `PitchDeckRequest` | `idea`, `product_description` (optional), `model` |
| `AutoDetectRequest` | `message` (str, min 5), `model`, `context` (optional dict) |

### Response Models
| Model | Fields |
|-------|--------|
| `GenerationResponse` | `feature`, `content`, `model_used`, `tokens_used` (optional int) |
| `AutoDetectResponse` | `detected_feature`, `content`, `model_used` |
| `HealthResponse` | `status`, `service`, `version`, `nova_models` (dict) |

---

## 11. FILE COUNT SUMMARY

| Category | Files | Lines (approx) |
|----------|-------|-----------------|
| Backend Python | 8 | ~1,000 |
| Backend Config | 3 | ~40 |
| Frontend JSX Components | 7 | ~625 |
| Frontend CSS Stylesheets | 7 | ~800 |
| Frontend Services | 1 | ~144 |
| Frontend Config | 4 | ~80 |
| Project Documentation | 2 | ~480+ |
| **Total** | **32+ files** | **~3,100+ lines** |

---

## 12. HOW TO RUN

### Prerequisites
- Python 3.11+
- Node.js 18+
- AWS Account with Bedrock access (Nova models enabled in us-east-1)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate          # macOS/Linux
pip install -r requirements.txt
# Edit .env with your AWS credentials
python run.py
# → http://localhost:8000  (API docs: http://localhost:8000/docs)
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

**Or use VS Code tasks:** `Cmd+Shift+B` → "Start All (Backend + Frontend)"

---

## 13. WHAT'S NEEDED TO GO LIVE

| Step | Status |
|------|--------|
| Add real AWS credentials in `backend/.env` | ⬜ Required |
| Enable Nova models in AWS Bedrock console (us-east-1) | ⬜ Required |
| Install backend dependencies (`pip install -r requirements.txt`) | ⬜ Required |
| Install frontend dependencies (`npm install`) | ⬜ Required |
| Everything else | ✅ Ready to demo |

---

## 14. RECENT IMPROVEMENTS (Iteration Log)

| # | Category | Improvement |
|---|----------|-------------|
| 1 | 🚀 Model | Added **Nova Premier** (`amazon.nova-premier-v1:0`) as the most powerful model option and new default |
| 2 | 🔒 Security | Added **rate limiting** (`slowapi`, 10 req/min per IP) on all generation endpoints |
| 3 | ⚡ Performance | Wrapped blocking `boto3` calls in **`run_in_executor`** to prevent async event loop blocking |
| 4 | 📊 Feature | **Token usage tracking** — extracts from Bedrock invocation metrics, displayed in UI |
| 5 | 🎨 UX | **Framer Motion** animations on feature cards (stagger, hover scale, tap feedback) |
| 6 | 💾 UX | **Persistent history** via `localStorage` (survives page refresh, keeps last 10) |
| 7 | 🐛 Error UX | **User-friendly error messages** for validation (422) and rate limiting (429) |
| 8 | 🏗️ Code | Extracted **`_build_body()`** helper to eliminate duplicated request building |
| 9 | 🔧 DevEx | Added `/health` to Vite proxy config for full dev parity |
| 10 | 📝 Docs | Updated all docs, footer, and docstrings to reflect 4-model lineup |

---

**End of Report**  
*Founder Copilot — Amazon Nova AI Hackathon 2026*  
*Full-stack AI application: 32+ files · 3,100+ lines · 4 Nova models · 6 API endpoints · Production-ready*
