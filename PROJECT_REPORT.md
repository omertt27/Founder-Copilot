# 📋 FOUNDER COPILOT — PROJECT REPORT
### Amazon Nova AI Hackathon — Build Report
**Date:** March 7, 2026  
**Project:** Founder Copilot — AI-Powered Startup Helper Agent  
**Team Stack:** Amazon Nova AI (Bedrock) + FastAPI + React/Vite

---

## 1. PROJECT OVERVIEW

**Founder Copilot** is a full-stack web application that helps startup founders turn raw ideas into actionable plans using Amazon Nova AI. The app provides four core AI-powered features, each driven by carefully optimized prompts targeting Amazon Nova's Pro, Lite, and Micro models through Amazon Bedrock.

**Hackathon Goal:** Demonstrate the power of Amazon Nova AI models for real-world startup tooling — from ideation to investor pitch.

---

## 2. WHAT WAS BUILT

### 2.1 Complete Backend (Python / FastAPI)

| File | Purpose | Lines |
|------|---------|-------|
| `backend/app/main.py` | FastAPI application entry point, CORS middleware, health checks | 67 |
| `backend/app/config.py` | Environment variable loader, AWS/Nova model settings | ~40 |
| `backend/app/nova_client.py` | Amazon Bedrock client — handles invoke + streaming for all 3 Nova models | 134 |
| `backend/app/prompts.py` | All 5 prompt templates optimized for Amazon Nova AI | ~250 |
| `backend/app/models.py` | Pydantic request/response schemas (7 models) | ~90 |
| `backend/app/routes.py` | 6 API route handlers with full error handling | ~270 |
| `backend/app/__init__.py` | Package initializer | 3 |
| `backend/run.py` | Server runner (uvicorn with hot-reload) | 12 |
| `backend/requirements.txt` | Python dependencies | 7 |
| `backend/.env` / `.env.example` | Environment config templates | 12 |

**Backend Dependencies Installed:**
- `fastapi==0.115.6` — Web framework
- `uvicorn[standard]==0.34.0` — ASGI server
- `boto3==1.36.2` — AWS SDK (Bedrock access)
- `python-dotenv==1.0.1` — Environment config
- `pydantic==2.10.5` — Data validation
- `mangum==0.19.0` — AWS Lambda adapter (deployment-ready)
- `python-multipart==0.0.20` — Form data support

---

### 2.2 Complete Frontend (React / Vite)

| File | Purpose | Description |
|------|---------|-------------|
| **Core** | | |
| `frontend/src/main.jsx` | React entry point | Mounts app to DOM |
| `frontend/src/App.jsx` | Main app component | State management, feature orchestration, layout |
| `frontend/src/App.css` | App-level styles | Hero section, error banner, footer |
| `frontend/src/index.css` | Global CSS | Design system (colors, typography, animations, markdown rendering) |
| **Components** | | |
| `frontend/src/components/Header.jsx` + `.css` | Top navigation bar | Brand logo, "Amazon Nova Hackathon" badge |
| `frontend/src/components/FeatureCards.jsx` + `.css` | Feature selector grid | 4 cards with icons, colors, selection state |
| `frontend/src/components/InputPanel.jsx` + `.css` | User input form | Textarea, model selector (Pro/Lite/Micro), generate button |
| `frontend/src/components/OutputPanel.jsx` + `.css` | Result renderer | Markdown display, copy-to-clipboard, download-as-MD |
| `frontend/src/components/LoadingSkeleton.jsx` + `.css` | Loading state | Animated skeleton lines + rotating status messages |
| `frontend/src/components/History.jsx` + `.css` | Generation history | Session history with feature icons, click to re-view |
| **Services** | | |
| `frontend/src/services/api.js` | API client | All backend calls, SSE streaming support, error handling |
| **Config** | | |
| `frontend/vite.config.js` | Vite configuration | Dev server on :5173, proxy `/api` → backend :8000 |
| `frontend/index.html` | HTML shell | Google Fonts (Inter + JetBrains Mono), meta tags |
| `frontend/package.json` | NPM config | Dependencies + scripts |
| `frontend/public/rocket.svg` | Favicon | Rocket emoji SVG |

**Frontend Dependencies Installed:**
- `react@18.3.1` + `react-dom@18.3.1` — UI framework
- `react-markdown@9.0.1` — Markdown rendering for AI output
- `react-icons@5.4.0` — Icon library (Heroicons v2)
- `framer-motion@11.15.0` — Animations
- `vite@6.0.7` + `@vitejs/plugin-react` — Build tooling

---

### 2.3 Project Infrastructure

| File | Purpose |
|------|---------|
| `README.md` | Full project documentation with setup guide, API reference, demo examples |
| `.gitignore` | Ignores node_modules, venv, .env, build artifacts, IDE files |
| `.vscode/tasks.json` | 3 VS Code tasks: Backend, Frontend, Start All (parallel) |

---

## 3. FEATURES IMPLEMENTED

### Feature 1: 💡 Startup Plan Generator
- **Endpoint:** `POST /api/generate/startup-plan`
- **Input:** Startup idea (free text)
- **Output:** 6-section plan — Product Description, Target Users, MVP Features, 6-Month Roadmap, Success Metrics, Potential Challenges
- **Temperature:** 0.3 (focused/structured)

### Feature 2: 🏗️ Technical Architecture Generator
- **Endpoint:** `POST /api/generate/tech-architecture`
- **Input:** Product description
- **Output:** 6-section architecture — Tech Stack (with reasoning), System Architecture Diagram, Database Schema, API Endpoints, Security Considerations, Scalability Notes
- **Temperature:** 0.3 (precise/technical)

### Feature 3: 📋 GitHub Issues Generator
- **Endpoint:** `POST /api/generate/github-issues`
- **Input:** Product name + description + tech stack
- **Output:** 15-20 prioritized issues with titles, priority levels, time estimates, descriptions, acceptance criteria, labels, and technical notes
- **Temperature:** 0.3 (structured)

### Feature 4: 🎤 Pitch Deck Generator
- **Endpoint:** `POST /api/generate/pitch-deck`
- **Input:** Startup idea + optional description
- **Output:** 12-slide investor-ready pitch deck — Cover, Problem, Solution, How It Works, Market Opportunity, Business Model, Traction, Competition, GTM Strategy, Team, Financials, The Ask
- **Temperature:** 0.7 (more creative)

### Feature 5: 🤖 Smart Auto-Detect (Agent Coordinator)
- **Endpoint:** `POST /api/generate/auto`
- **How it works:** Uses Nova Micro (fastest, cheapest) to classify user intent → then routes to the correct feature using Nova Pro for full generation
- **Two-step AI pipeline** — demonstrates multi-model orchestration

### Feature 6: 📡 Streaming Endpoint
- **Endpoint:** `POST /api/generate/stream/{feature}`
- **Output:** Server-Sent Events (SSE) for real-time text streaming
- **Supports all 4 features** with appropriate temperature per feature type

---

## 4. AMAZON NOVA AI INTEGRATION

### Models Used
| Model | ID | Use Case |
|-------|-----|----------|
| **Nova Pro** | `amazon.nova-pro-v1:0` | Primary generation (highest quality) |
| **Nova Lite** | `amazon.nova-lite-v1:0` | Balanced speed/quality option |
| **Nova Micro** | `amazon.nova-micro-v1:0` | Intent detection (fastest, agent coordinator) |

### Bedrock Integration Details
- **Client:** `boto3` → `bedrock-runtime` service
- **API:** `invoke_model` (sync) + `invoke_model_with_response_stream` (streaming)
- **Request Format:** Nova `messages-v1` schema with system prompt + user messages
- **Inference Config:** Configurable `temperature`, `max_new_tokens`, `topP`
- **Retry Strategy:** Adaptive mode with 3 max attempts
- **Error Handling:** Full try/catch with HTTP 500 responses

### Prompt Engineering
- 5 optimized prompt templates totaling ~250 lines
- Each prompt uses **role-based instruction** (e.g., "You are a senior software architect...")
- **Section-by-section output formatting** for structured Markdown
- **Shared system prompt** across all features for consistent tone
- **Agent coordinator prompt** returns only classification tokens for fast routing

---

## 5. UI/UX DESIGN

### Design System
- **Theme:** Dark mode with purple/pink accent gradient
- **Fonts:** Inter (body), JetBrains Mono (code)
- **Colors:** Deep navy background (#0a0a0f), purple primary (#6c63ff), pink secondary (#ff6b9d)
- **Each feature has its own color identity:**
  - Startup Plan → Purple (#6c63ff)
  - Tech Architecture → Cyan (#00d2ff)
  - GitHub Issues → Green (#4ade80)
  - Pitch Deck → Pink (#ff6b9d)

### UX Features
- ✅ Feature selection via interactive cards
- ✅ Nova model selector (Pro / Lite / Micro) per request
- ✅ Rich Markdown rendering of AI output (headers, lists, tables, code blocks, checkboxes)
- ✅ Copy to clipboard
- ✅ Download as `.md` file
- ✅ Animated loading skeleton with rotating status messages
- ✅ Session history — click to re-view any previous generation
- ✅ Responsive layout (mobile → desktop)
- ✅ Custom scrollbar, selection highlight, smooth animations

---

## 6. API REFERENCE

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check (JSON) |
| `GET` | `/health` | Health check (JSON) |
| `GET` | `/docs` | Swagger UI (auto-generated) |
| `GET` | `/redoc` | ReDoc documentation |
| `POST` | `/api/generate/startup-plan` | Generate startup plan |
| `POST` | `/api/generate/tech-architecture` | Generate tech architecture |
| `POST` | `/api/generate/github-issues` | Generate GitHub issues |
| `POST` | `/api/generate/pitch-deck` | Generate pitch deck |
| `POST` | `/api/generate/auto` | Auto-detect intent + generate |
| `POST` | `/api/generate/stream/{feature}` | SSE streaming generation |

---

## 7. FILE COUNT SUMMARY

| Category | Files | Description |
|----------|-------|-------------|
| Backend Python | 8 | FastAPI app, routes, models, prompts, client, config |
| Backend Config | 4 | requirements.txt, .env, .env.example, run.py |
| Frontend JSX | 7 | App + 6 components |
| Frontend CSS | 7 | App + 6 component stylesheets |
| Frontend Services | 1 | API client |
| Frontend Config | 4 | package.json, vite.config.js, index.html, favicon |
| Project Root | 3 | README.md, .gitignore, .vscode/tasks.json |
| **Total** | **34 files** | **Complete full-stack application** |

---

## 8. HOW TO RUN

```bash
# Backend
cd backend
source venv/bin/activate
python run.py
# → http://localhost:8000

# Frontend
cd frontend
npm run dev
# → http://localhost:5173
```

**Or use VS Code tasks:** `Cmd+Shift+B` → "Start All (Backend + Frontend)"

---

## 9. WHAT'S NEEDED TO GO LIVE

1. **Add real AWS credentials** in `backend/.env`
2. **Enable Nova models** in AWS Bedrock console (us-east-1)
3. Everything else is ready to demo

---

## 10. ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React/Vite)                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ Startup  │ │  Tech    │ │  GitHub  │ │  Pitch   │   │
│  │  Plan    │ │  Arch    │ │  Issues  │ │  Deck    │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │
│       └─────────────┼───────────┼─────────────┘         │
│                     ▼           ▼                        │
│              ┌─────────────────────┐                     │
│              │    API Service      │                     │
│              │   (api.js)          │                     │
│              └──────────┬──────────┘                     │
└─────────────────────────┼───────────────────────────────┘
                          │ HTTP/SSE (proxy :5173→:8000)
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                        │
│  ┌──────────────────────────────────────────────┐        │
│  │              routes.py                        │        │
│  │  POST /startup-plan   POST /tech-architecture│        │
│  │  POST /github-issues  POST /pitch-deck       │        │
│  │  POST /auto (agent)   POST /stream/{feature} │        │
│  └──────────────────┬───────────────────────────┘        │
│                     ▼                                    │
│  ┌──────────────────────────────────────────────┐        │
│  │           prompts.py (5 templates)           │        │
│  └──────────────────┬───────────────────────────┘        │
│                     ▼                                    │
│  ┌──────────────────────────────────────────────┐        │
│  │         nova_client.py (Bedrock Client)       │        │
│  │    invoke() + invoke_streaming()              │        │
│  └──────────────────┬───────────────────────────┘        │
└─────────────────────┼───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│              AMAZON BEDROCK                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Nova Pro │  │ Nova Lite│  │Nova Micro│              │
│  │ (quality)│  │(balanced)│  │ (fast)   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

---

**End of Report**  
*Founder Copilot — Amazon Nova AI Hackathon 2026*
