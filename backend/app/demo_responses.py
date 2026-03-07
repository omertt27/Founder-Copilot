"""
Founder Copilot - Demo Responses
Realistic sample outputs for running without AWS credentials.
These demonstrate exactly what the app produces with real Nova models.
"""

import asyncio
import random

DEMO_STARTUP_PLAN = """# 💡 Startup Plan: AI-Powered Meeting Assistant

## 1. Product Description

**MeetingAI** is an intelligent meeting assistant that automatically records, transcribes, and summarizes business meetings — then generates structured action items with assigned owners and deadlines. It integrates with Zoom, Google Meet, and Microsoft Teams.

**Who is it for?** Remote and hybrid teams who spend 15+ hours/week in meetings.
**What problem does it solve?** Eliminates the need for manual note-taking, ensures nothing falls through the cracks, and saves teams ~5 hours/week per person.

---

## 2. Target Users

### Primary Audience
- **Engineering Managers** (25-45) at mid-size tech companies (50-500 employees)
- **Product Managers** who run 8-12 meetings/week
- **Team Leads** managing remote/hybrid teams across time zones

### Secondary Audience
- **Executive Assistants** preparing meeting briefs
- **Sales Teams** needing call summaries and CRM updates
- **Consultants** documenting client meetings

### Pain Points Solved
- ❌ "I forgot what was decided in last week's standup"
- ❌ "Who was supposed to follow up on that action item?"
- ❌ "I spent 30 minutes writing meeting notes instead of doing actual work"

---

## 3. MVP Features (Minimum Viable Product)

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Meeting Recording** | One-click recording with auto-join for scheduled meetings |
| 2 | **AI Transcription** | Real-time speech-to-text with speaker identification |
| 3 | **Smart Summaries** | AI-generated executive summaries with key decisions highlighted |
| 4 | **Action Item Extraction** | Automatically detects commitments and assigns owners + deadlines |
| 5 | **Searchable Archive** | Full-text search across all past meetings |
| 6 | **Slack/Teams Integration** | Auto-posts summaries to the relevant channel |
| 7 | **Dashboard** | Team overview showing meeting load, pending action items, and trends |

---

## 4. 6-Month Roadmap

### Month 1-2: MVP Development 🏗️
- [ ] Set up core transcription pipeline (AWS Transcribe + Nova)
- [ ] Build meeting recording engine (WebRTC)
- [ ] Create action item extraction model
- [ ] Deploy basic web dashboard
- **Milestone:** Internal dogfooding with 5 test users

### Month 3-4: Beta Launch 🚀
- [ ] Launch private beta with 50 teams
- [ ] Add Zoom + Google Meet integrations
- [ ] Implement summary quality feedback loop
- [ ] Set up usage analytics and monitoring
- **Milestone:** 50 active teams, NPS > 40

### Month 5-6: Growth 📈
- [ ] Public launch on Product Hunt
- [ ] Add Microsoft Teams integration
- [ ] Implement team analytics dashboard
- [ ] Launch freemium tier + Pro plan ($15/user/month)
- **Milestone:** 500 active teams, $10K MRR

---

## 5. Success Metrics

| Metric | Target (6 months) |
|--------|-------------------|
| Active Teams | 500+ |
| Daily Active Users | 2,000+ |
| Meetings Processed/Day | 1,000+ |
| Action Item Accuracy | > 85% |
| NPS Score | > 50 |
| Monthly Recurring Revenue | $10,000+ |
| User Retention (30-day) | > 70% |

---

## 6. Potential Challenges

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Audio quality varies wildly** | Low transcription accuracy | Multi-model pipeline with noise cancellation + fallback to manual review |
| **Enterprise security concerns** | Blocks B2B adoption | SOC 2 compliance from Day 1, end-to-end encryption, on-prem option |
| **Crowded market (Otter.ai, Fireflies)** | Hard to differentiate | Focus on action items + team workflows, not just transcription |
"""

DEMO_TECH_ARCHITECTURE = """# 🏗️ Technical Architecture: AI Meeting Assistant

## 1. Recommended Tech Stack

### Frontend
| Layer | Choice | Reasoning |
|-------|--------|-----------|
| **Framework** | Next.js 14 (App Router) | SSR for SEO, React Server Components for performance |
| **UI Library** | shadcn/ui + Tailwind CSS | Modern, accessible, customizable components |
| **State Management** | Zustand + React Query | Lightweight global state + server state caching |
| **Real-time** | Socket.io client | Live transcription updates during meetings |

### Backend
| Layer | Choice | Reasoning |
|-------|--------|-----------|
| **Framework** | FastAPI (Python) | Async-first, excellent for AI/ML workloads |
| **Language** | Python 3.11+ | Best AI/ML ecosystem, boto3 native |
| **API Type** | REST + WebSocket | REST for CRUD, WebSocket for live transcription |
| **Task Queue** | Celery + Redis | Async processing of recordings and AI summaries |

### AI / ML
| Layer | Choice | Reasoning |
|-------|--------|-----------|
| **Transcription** | Amazon Transcribe | Real-time streaming, speaker diarization |
| **Summarization** | Amazon Nova Premier | Best quality for structured output |
| **Intent Detection** | Amazon Nova Micro | Fast action item classification |
| **Embeddings** | Amazon Titan Embeddings | Semantic search across meetings |

### Database
| Layer | Choice | Reasoning |
|-------|--------|-----------|
| **Primary DB** | PostgreSQL (RDS) | Relational data: users, teams, meetings |
| **Vector DB** | Amazon OpenSearch | Semantic search + meeting embeddings |
| **Cache** | Redis (ElastiCache) | Session management + real-time state |
| **Object Storage** | S3 | Audio recordings + transcripts |

### Infrastructure
| Layer | Choice | Reasoning |
|-------|--------|-----------|
| **Hosting** | AWS (ECS Fargate) | Serverless containers, auto-scaling |
| **CI/CD** | GitHub Actions → ECR → ECS | Automated build/test/deploy pipeline |
| **CDN** | CloudFront | Static assets + global latency reduction |
| **Monitoring** | CloudWatch + Sentry | Logs, metrics, error tracking |

---

## 2. System Architecture

```
┌──────────────────────────────────┐
│         Client (Next.js)         │
│  • Dashboard  • Meeting View     │
│  • Search     • Settings         │
└──────────┬───────────────────────┘
           │ HTTPS / WebSocket
           ▼
┌──────────────────────────────────┐
│      API Gateway (FastAPI)       │
│  • Auth middleware (JWT)         │
│  • Rate limiting                 │
│  • Request validation            │
└──────┬───────────┬───────────────┘
       │           │
       ▼           ▼
┌─────────────┐ ┌──────────────────┐
│ PostgreSQL  │ │  Celery Workers   │
│  (Users,    │ │  • Transcription  │
│   Meetings, │ │  • Summarization  │
│   Actions)  │ │  • Action Extract │
└─────────────┘ └────────┬─────────┘
                         │
                         ▼
              ┌────────────────────┐
              │  Amazon Bedrock    │
              │  Nova Premier/Pro  │
              │  + Transcribe      │
              └────────────────────┘
```

---

## 3. Database Schema

### Table: `users`
| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID (PK) | Auto-generated |
| `email` | VARCHAR(255) | Unique, indexed |
| `name` | VARCHAR(100) | Display name |
| `team_id` | UUID (FK) | References `teams.id` |
| `role` | ENUM | admin, member |
| `created_at` | TIMESTAMP | Default: now() |

### Table: `meetings`
| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID (PK) | Auto-generated |
| `title` | VARCHAR(255) | Meeting title |
| `team_id` | UUID (FK) | References `teams.id` |
| `recording_url` | TEXT | S3 URL |
| `transcript` | TEXT | Full transcript |
| `summary` | TEXT | AI-generated summary |
| `duration_seconds` | INT | Meeting length |
| `status` | ENUM | recording, processing, ready |
| `created_at` | TIMESTAMP | Meeting start time |

### Table: `action_items`
| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID (PK) | Auto-generated |
| `meeting_id` | UUID (FK) | References `meetings.id` |
| `assignee_id` | UUID (FK) | References `users.id` |
| `description` | TEXT | What needs to be done |
| `deadline` | DATE | When it's due |
| `status` | ENUM | pending, done, overdue |
| `confidence` | FLOAT | AI confidence score (0-1) |

---

## 4. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/signup` | Create account |
| `POST` | `/api/auth/login` | Login (returns JWT) |
| `GET` | `/api/meetings` | List team meetings |
| `POST` | `/api/meetings` | Start new meeting |
| `GET` | `/api/meetings/:id` | Get meeting details |
| `GET` | `/api/meetings/:id/transcript` | Get full transcript |
| `GET` | `/api/meetings/:id/actions` | List action items |
| `PATCH` | `/api/actions/:id` | Update action item status |
| `GET` | `/api/search?q=` | Semantic search across meetings |
| `GET` | `/api/analytics/team` | Team meeting analytics |

---

## 5. Security Considerations

- **Authentication:** JWT tokens with refresh rotation (15min access, 7d refresh)
- **Authorization:** Role-based access control (RBAC) — admin, member, viewer
- **Data Encryption:** AES-256 at rest, TLS 1.3 in transit
- **Audio Privacy:** Recordings auto-delete after 90 days (configurable)
- **API Security:** Rate limiting (100 req/min), input sanitization, CORS whitelist
- **Compliance:** SOC 2 Type II readiness from Day 1

---

## 6. Scalability Notes

- **Horizontal scaling:** ECS Fargate auto-scales containers based on CPU/memory
- **Database:** Read replicas for search-heavy queries, connection pooling via PgBouncer
- **Bottleneck:** AI processing (transcription + summarization) — mitigated by Celery worker pool
- **Cost optimization:** Spot instances for Celery workers, S3 lifecycle policies for old recordings
"""

DEMO_GITHUB_ISSUES = """# 📋 GitHub Issues: Development Backlog

---

### Issue #1: Project Setup & Repository Structure
**Priority:** High
**Estimate:** Small (1-2 days)
**Labels:** `setup`, `infrastructure`

**Description:**
Initialize the monorepo with the backend (FastAPI) and frontend (Next.js) projects. Set up linting, formatting, and pre-commit hooks.

**Acceptance Criteria:**
- [ ] Repository initialized with README, .gitignore, and LICENSE
- [ ] Backend project scaffolded with FastAPI, uvicorn, and pyproject.toml
- [ ] Frontend project scaffolded with Next.js 14, TypeScript, and Tailwind
- [ ] ESLint + Prettier configured for frontend
- [ ] Ruff + Black configured for backend
- [ ] Pre-commit hooks running on both projects

**Technical Notes:**
Use a monorepo structure with `/backend` and `/frontend` directories. Consider using Turborepo for build orchestration.

---

### Issue #2: Database Setup & Migrations
**Priority:** High
**Estimate:** Small (1-2 days)
**Labels:** `setup`, `backend`, `database`

**Description:**
Set up PostgreSQL with SQLAlchemy ORM and Alembic for migrations. Create initial schema for users, teams, meetings, and action items.

**Acceptance Criteria:**
- [ ] PostgreSQL connection configured via environment variables
- [ ] SQLAlchemy models for all 4 core tables (users, teams, meetings, action_items)
- [ ] Alembic migration setup with initial migration
- [ ] Database seeder for development data
- [ ] Docker Compose file for local PostgreSQL

**Technical Notes:**
Use async SQLAlchemy (asyncpg driver) for compatibility with FastAPI's async handlers.

---

### Issue #3: Authentication System (JWT)
**Priority:** High
**Estimate:** Medium (3-5 days)
**Labels:** `feature`, `backend`, `security`

**Description:**
Implement JWT-based authentication with signup, login, token refresh, and password reset flows.

**Acceptance Criteria:**
- [ ] `POST /api/auth/signup` — creates user with hashed password
- [ ] `POST /api/auth/login` — returns access + refresh tokens
- [ ] `POST /api/auth/refresh` — rotates tokens
- [ ] Password hashing with bcrypt
- [ ] Protected route middleware
- [ ] Unit tests for all auth endpoints

**Technical Notes:**
Use `python-jose` for JWT encoding. Access tokens: 15min expiry. Refresh tokens: 7 days with rotation.

---

### Issue #4: Meeting Recording Engine
**Priority:** High
**Estimate:** Large (1-2 weeks)
**Labels:** `feature`, `backend`, `core`

**Description:**
Build the core meeting recording system that captures audio from WebRTC streams and stores in S3.

**Acceptance Criteria:**
- [ ] WebRTC audio capture from browser
- [ ] Server-side audio processing and encoding
- [ ] S3 upload with presigned URLs
- [ ] Recording status tracking (recording → processing → ready)
- [ ] Maximum recording duration: 4 hours

---

### Issue #5: AI Transcription Pipeline
**Priority:** High
**Estimate:** Large (1-2 weeks)
**Labels:** `feature`, `backend`, `ai`

**Description:**
Integrate Amazon Transcribe for real-time speech-to-text with speaker diarization.

**Acceptance Criteria:**
- [ ] Streaming transcription via Amazon Transcribe
- [ ] Speaker identification (up to 10 speakers)
- [ ] Timestamp alignment for transcript segments
- [ ] WebSocket push to frontend for live updates
- [ ] Fallback to batch processing for failed streams

---

### Issue #6: AI Summary Generation
**Priority:** High
**Estimate:** Medium (3-5 days)
**Labels:** `feature`, `backend`, `ai`

**Description:**
Use Amazon Nova Premier to generate structured meeting summaries from transcripts.

**Acceptance Criteria:**
- [ ] Summary includes: key decisions, discussion topics, next steps
- [ ] Processing triggered automatically when transcription completes
- [ ] Summary stored in meetings table
- [ ] Quality feedback mechanism (thumbs up/down)

---

### Issue #7: Action Item Extraction
**Priority:** High
**Estimate:** Medium (3-5 days)
**Labels:** `feature`, `backend`, `ai`

**Description:**
Extract action items from meeting transcripts using Nova, including assignee detection and deadline inference.

**Acceptance Criteria:**
- [ ] Detects commitments like "I'll do X by Friday"
- [ ] Maps to team members when possible
- [ ] Assigns confidence scores (0-1)
- [ ] CRUD API for action items
- [ ] Slack notification for new action items

---

### Issue #8: Dashboard UI — Meeting List
**Priority:** High
**Estimate:** Medium (3-5 days)
**Labels:** `feature`, `frontend`

**Description:**
Build the main dashboard page showing all team meetings with summaries, action items, and search.

**Acceptance Criteria:**
- [ ] List view of meetings sorted by date
- [ ] Each card shows: title, date, duration, # action items, summary preview
- [ ] Click to view full meeting details
- [ ] Responsive design (mobile + desktop)

---

### Issue #9: Meeting Detail Page
**Priority:** Medium
**Estimate:** Medium (3-5 days)
**Labels:** `feature`, `frontend`

**Description:**
Build the meeting detail view with transcript, summary, action items, and audio playback.

**Acceptance Criteria:**
- [ ] Full transcript with speaker labels and timestamps
- [ ] AI summary with key decisions highlighted
- [ ] Action items checklist with assign/complete
- [ ] Audio player synced to transcript

---

### Issue #10: Semantic Search
**Priority:** Medium
**Estimate:** Medium (3-5 days)
**Labels:** `feature`, `backend`, `frontend`

**Description:**
Implement full-text and semantic search across all meetings and transcripts.

**Acceptance Criteria:**
- [ ] Search bar in dashboard header
- [ ] Results show matching meetings with highlighted excerpts
- [ ] Semantic search using Amazon Titan embeddings
- [ ] Search result relevance ranking

---

### Issue #11: Zoom Integration
**Priority:** Medium
**Estimate:** Large (1-2 weeks)
**Labels:** `feature`, `integration`

**Description:**
Build Zoom OAuth integration for automatic meeting joining and recording.

**Acceptance Criteria:**
- [ ] Zoom OAuth2 flow for authorization
- [ ] Auto-detect scheduled Zoom meetings
- [ ] Bot joins meeting and records audio
- [ ] Handle meeting end → trigger transcription pipeline

---

### Issue #12: Slack Integration
**Priority:** Medium
**Estimate:** Medium (3-5 days)
**Labels:** `feature`, `integration`

**Description:**
Post meeting summaries and action items to Slack channels automatically.

**Acceptance Criteria:**
- [ ] Slack OAuth2 integration
- [ ] Channel mapping (meeting → Slack channel)
- [ ] Auto-post summary when processing completes
- [ ] `/meetingai` slash command for quick search

---

### Issue #13: Team Analytics Dashboard
**Priority:** Low
**Estimate:** Medium (3-5 days)
**Labels:** `feature`, `frontend`

**Description:**
Build analytics page showing meeting patterns, action item completion rates, and time spent.

**Acceptance Criteria:**
- [ ] Meeting frequency chart (meetings/week)
- [ ] Action item completion rate
- [ ] Average meeting duration trend
- [ ] Top contributors (most action items completed)

---

### Issue #14: Responsive Design & Mobile Optimization
**Priority:** Medium
**Estimate:** Small (1-2 days)
**Labels:** `ui`, `frontend`

**Description:**
Ensure all pages are fully responsive and usable on mobile devices.

**Acceptance Criteria:**
- [ ] Dashboard works on screens ≥ 375px wide
- [ ] Meeting detail collapses to single column on mobile
- [ ] Touch-friendly action item checkboxes
- [ ] Tested on iOS Safari and Android Chrome

---

### Issue #15: Unit & Integration Tests
**Priority:** Medium
**Estimate:** Medium (3-5 days)
**Labels:** `testing`, `backend`

**Description:**
Write comprehensive tests for API endpoints, auth flows, and AI pipelines.

**Acceptance Criteria:**
- [ ] pytest test suite with > 80% coverage on API routes
- [ ] Auth flow integration tests
- [ ] Mock Bedrock responses for AI tests
- [ ] CI/CD pipeline runs tests on every PR

---

### Issue #16: CI/CD Pipeline
**Priority:** High
**Estimate:** Small (1-2 days)
**Labels:** `infrastructure`, `devops`

**Description:**
Set up GitHub Actions for automated testing, building, and deploying to AWS.

**Acceptance Criteria:**
- [ ] On PR: lint + test + build
- [ ] On merge to main: deploy to staging
- [ ] On release tag: deploy to production
- [ ] Docker build for backend + frontend

---

### Issue #17: Rate Limiting & Abuse Prevention
**Priority:** Medium
**Estimate:** Small (1-2 days)
**Labels:** `security`, `backend`

**Description:**
Add rate limiting to prevent API abuse and control AI generation costs.

**Acceptance Criteria:**
- [ ] Per-user rate limits (10 meetings/day free tier)
- [ ] Per-IP rate limiting on auth endpoints
- [ ] Graceful error messages for exceeded limits
- [ ] Admin override for enterprise accounts
"""

DEMO_PITCH_DECK = """# 🎤 Pitch Deck: MeetingAI

---

## Slide 1: Cover
### **MeetingAI**
*"Never miss an action item again."*

**Tagline:** AI-powered meeting assistant that records, summarizes, and creates action items — so your team can focus on doing, not documenting.

**Visual suggestion:** Clean logo on dark gradient background with a subtle waveform animation.

---

## Slide 2: The Problem 😤
### Meetings are broken.

- **$37 billion** is lost annually to unproductive meetings (Harvard Business Review)
- The average professional attends **15+ meetings/week** and spends **4 hours writing notes**
- **73%** of professionals do other work during meetings because they know no one will follow up
- Action items from meetings have a **< 30% completion rate** without tracking

> *"I can't remember what we decided in last Tuesday's standup, and neither can anyone else."*

**Visual suggestion:** Pain point statistics in large, bold typography. Red/orange tones.

---

## Slide 3: The Solution 💡
### MeetingAI: Your Intelligent Meeting Copilot

MeetingAI joins your meetings automatically, listens in real-time, and delivers:
1. **🎙️ Perfect Transcripts** — with speaker identification
2. **📝 Smart Summaries** — key decisions + discussion topics in 30 seconds
3. **✅ Auto-Extracted Action Items** — with owners, deadlines, and Slack notifications

> It's like having a perfect note-taker in every meeting — powered by Amazon Nova AI.

**Visual suggestion:** Product screenshot showing a meeting summary with highlighted action items.

---

## Slide 4: How It Works ⚡
### 3 Simple Steps

| Step | Action | Time |
|------|--------|------|
| 1️⃣ | **Connect** — Link your Zoom/Meet/Teams calendar | 2 min setup |
| 2️⃣ | **Meet** — MeetingAI auto-joins and records | Zero effort |
| 3️⃣ | **Act** — Get summary + action items in Slack | Instant |

**Visual suggestion:** Horizontal flow diagram with icons for each step.

---

## Slide 5: Market Opportunity 📊
### $15.8B Meeting Management Market (2025)

| Segment | Size | Growth |
|---------|------|--------|
| **TAM** (Total Addressable Market) | $15.8B | Meeting management software |
| **SAM** (Serviceable Available Market) | $4.2B | AI-powered meeting tools |
| **SOM** (Serviceable Obtainable Market) | $120M | Remote-first teams (50-500 employees) |

- Remote work grew **300%** since 2020
- AI productivity tools market growing at **34% CAGR**
- Enterprise spending on collaboration tools: **$45B/year**

**Visual suggestion:** Concentric circles showing TAM → SAM → SOM with dollar amounts.

---

## Slide 6: Business Model 💰
### SaaS — Per-User Monthly Subscription

| Tier | Price | Includes |
|------|-------|----------|
| **Free** | $0/user/mo | 5 meetings/month, basic summaries |
| **Pro** | $15/user/mo | Unlimited meetings, action items, integrations |
| **Enterprise** | $30/user/mo | SSO, admin controls, on-prem option, priority support |

**Revenue drivers:**
- Land with Free tier → expand to Pro within teams
- Enterprise upsell for compliance-heavy industries (finance, healthcare, legal)

**Visual suggestion:** Pricing table with the Pro tier highlighted.

---

## Slide 7: Traction 🚀
### Early Signals

| Metric | Value |
|--------|-------|
| **Beta waitlist** | 2,400+ signups in 3 weeks |
| **Design partners** | 8 companies (Series A-C startups) |
| **LOIs** | 3 enterprise LOIs ($150K combined ACV) |
| **Product Hunt** | #2 Product of the Day |
| **NPS** | 68 (beta users) |

**Visual suggestion:** Upward-trending chart with key milestones marked on timeline.

---

## Slide 8: Competition 🥊
### How We're Different

| Feature | MeetingAI | Otter.ai | Fireflies | Grain |
|---------|-----------|----------|-----------|-------|
| Real-time transcription | ✅ | ✅ | ✅ | ✅ |
| AI summaries | ✅ | ✅ | ✅ | ❌ |
| **Auto action items** | ✅ | ❌ | Partial | ❌ |
| **Deadline detection** | ✅ | ❌ | ❌ | ❌ |
| **Team workflow integration** | ✅ | ❌ | Partial | ❌ |
| Slack/Teams auto-post | ✅ | Partial | ✅ | ❌ |
| Enterprise (SOC 2) | ✅ | ✅ | ❌ | ❌ |

**Our moat:** We don't just transcribe — we **drive accountability** by turning conversations into tracked commitments.

---

## Slide 9: Go-to-Market Strategy 📣
### Product-Led Growth + Enterprise Sales

**Phase 1 (Month 1-3): Community Launch**
- Product Hunt + Hacker News launch
- Free tier for individual users
- SEO content: "Best meeting AI tools 2025"

**Phase 2 (Month 4-6): Team Expansion**
- Viral loop: "Shared by MeetingAI" in Slack posts
- Team invite flow (invite 3 → get Pro free for a month)
- Partnerships with productivity YouTubers/newsletters

**Phase 3 (Month 7-12): Enterprise**
- Outbound sales to 200+ employee companies
- SOC 2 certification
- Channel partnerships with Zoom/Slack app marketplaces

**Visual suggestion:** Funnel showing Awareness → Free → Pro → Enterprise.

---

## Slide 10: Team 👥
### Why Us?

| Name | Role | Background |
|------|------|------------|
| **Sarah Chen** | CEO / Co-founder | Ex-PM at Zoom (4 yrs), Stanford CS |
| **Alex Rivera** | CTO / Co-founder | Ex-ML Engineer at Amazon (Alexa), MIT AI Lab |
| **Jordan Park** | Head of Design | Ex-Figma, designed for 50M+ users |

**Advisors:**
- Former VP of Product, Slack
- Partner at Andreessen Horowitz

**Visual suggestion:** Team photos with credential badges.

---

## Slide 11: Financials 💵
### 3-Year Revenue Projection

| Year | Users | ARR | Key Milestone |
|------|-------|-----|---------------|
| **Year 1** | 5,000 | $540K | Product-market fit, 50 paying teams |
| **Year 2** | 25,000 | $3.2M | Enterprise launch, 5 logo customers |
| **Year 3** | 100,000 | $12M | Market expansion, international |

**Key Assumptions:**
- 8% free → paid conversion rate
- $15 ARPU blended (Pro + Enterprise)
- 5% monthly churn (improving to 3% by Year 2)

**Visual suggestion:** Bar chart showing ARR growth Year 1 → Year 3.

---

## Slide 12: The Ask 🙏
### Raising $2.5M Seed Round

| Use of Funds | Allocation |
|--------------|------------|
| **Engineering** (4 hires) | 50% — $1.25M |
| **Go-to-Market** | 25% — $625K |
| **Infrastructure (AWS)** | 15% — $375K |
| **Operations** | 10% — $250K |

**Milestones this round will achieve:**
- ✅ Launch V1 with Zoom + Google Meet integration
- ✅ 5,000 users / 500 paying teams
- ✅ $500K ARR run rate
- ✅ SOC 2 Type II certification

> *"We're building the operating system for productive meetings. Let's make meetings worth having."*

**Visual suggestion:** Pie chart of fund allocation + milestone timeline.
"""


# Map feature types to demo responses
DEMO_RESPONSES = {
    "startup_plan": DEMO_STARTUP_PLAN,
    "tech_architecture": DEMO_TECH_ARCHITECTURE,
    "github_issues": DEMO_GITHUB_ISSUES,
    "pitch_deck": DEMO_PITCH_DECK,
}

# Simulated token counts (realistic for these lengths)
DEMO_TOKEN_COUNTS = {
    "startup_plan": 1847,
    "tech_architecture": 2156,
    "github_issues": 2934,
    "pitch_deck": 2512,
}

# Intent detection demo — returns a plausible feature based on keywords
INTENT_KEYWORDS = {
    "startup_plan": ["plan", "idea", "strategy", "startup", "roadmap", "validate", "mvp"],
    "tech_architecture": ["architecture", "tech", "stack", "database", "api", "build", "system", "backend", "frontend"],
    "github_issues": ["issues", "backlog", "sprint", "tasks", "development", "github", "jira"],
    "pitch_deck": ["pitch", "deck", "investor", "presentation", "funding", "raise"],
}


def detect_demo_intent(message: str) -> str:
    """Simple keyword-based intent detection for demo mode."""
    message_lower = message.lower()
    scores = {}
    for feature, keywords in INTENT_KEYWORDS.items():
        scores[feature] = sum(1 for kw in keywords if kw in message_lower)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "startup_plan"


async def get_demo_response(feature: str) -> tuple[str, int]:
    """Return a demo response with a realistic delay."""
    # Simulate 1-3 seconds of "thinking" to feel realistic
    await asyncio.sleep(random.uniform(1.0, 3.0))
    content = DEMO_RESPONSES.get(feature, DEMO_STARTUP_PLAN)
    tokens = DEMO_TOKEN_COUNTS.get(feature, 1500)
    return content, tokens


def stream_demo_response(feature: str):
    """Yield demo response in chunks for streaming, mimicking real Nova output."""
    content = DEMO_RESPONSES.get(feature, DEMO_STARTUP_PLAN)
    # Split into chunks of ~20-60 chars to simulate streaming
    words = content.split(" ")
    chunk = ""
    for word in words:
        chunk += word + " "
        if len(chunk) > random.randint(20, 60):
            yield chunk
            chunk = ""
    if chunk:
        yield chunk
