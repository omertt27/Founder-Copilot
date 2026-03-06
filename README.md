# 🚀 Founder Copilot

**AI-Powered Startup Helper Agent — Built for the Amazon Nova AI Hackathon**

Turn your startup idea into a comprehensive plan, technical architecture, development backlog, and investor-ready pitch deck — all powered by **Amazon Nova AI** through Amazon Bedrock.

![Amazon Nova AI](https://img.shields.io/badge/Amazon_Nova_AI-Powered-FF9900?style=for-the-badge&logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💡 **Startup Plan** | Comprehensive strategy with product description, target users, MVP features, 6-month roadmap, and success metrics |
| 🏗️ **Tech Architecture** | Full tech stack recommendation with database schema, API endpoints, security considerations |
| 📋 **GitHub Issues** | 15-20 prioritized development issues with estimates, acceptance criteria, and labels |
| 🎤 **Pitch Deck** | 12-slide investor-ready pitch deck outline with talking points and visual suggestions |

### 🤖 Amazon Nova Models Used

- **Nova Pro** — Best quality, comprehensive outputs
- **Nova Lite** — Balanced speed and quality
- **Nova Micro** — Fastest, used for intent detection

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11+** with **FastAPI**
- **Amazon Bedrock** (Nova Pro, Nova Lite, Nova Micro)
- **boto3** for AWS integration

### Frontend
- **React 18** with **Vite**
- **react-markdown** for rendering
- **Framer Motion** for animations
- **react-icons** for UI icons

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- AWS Account with Bedrock access (Nova models enabled)

### 1. Clone & Setup

```bash
cd "Founder Copilot"
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure AWS Credentials

Edit `backend/.env` with your AWS credentials:

```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
```

### 4. Start Backend

```bash
cd backend
python run.py
```

Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

### 5. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

---

## 📁 Project Structure

```
Founder Copilot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── config.py         # Environment & settings
│   │   ├── nova_client.py    # Amazon Nova/Bedrock client
│   │   ├── prompts.py        # All prompt templates
│   │   ├── models.py         # Pydantic schemas
│   │   └── routes.py         # API endpoints
│   ├── run.py                # Server runner
│   ├── requirements.txt
│   ├── .env                  # Your credentials (gitignored)
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API client
│   │   ├── App.jsx           # Main app
│   │   ├── App.css
│   │   ├── index.css         # Global styles
│   │   └── main.jsx          # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate/startup-plan` | Generate startup plan |
| `POST` | `/api/generate/tech-architecture` | Generate tech architecture |
| `POST` | `/api/generate/github-issues` | Generate GitHub issues |
| `POST` | `/api/generate/pitch-deck` | Generate pitch deck |
| `POST` | `/api/generate/auto` | Auto-detect & generate |
| `POST` | `/api/generate/stream/{feature}` | Streaming generation |
| `GET`  | `/health` | Health check |

---

## 🎬 Demo Examples

### Example 1: AI Meeting Assistant
```
"AI-powered meeting assistant that records meetings, generates summaries, 
and creates action items automatically"
```

### Example 2: Freelancer SaaS
```
"SaaS tool for freelancers to track time, send invoices, and manage clients"
```

### Example 3: AI Documentation Tool
```
"Developer tool that uses AI to automatically write documentation from code comments"
```

---

## 👨‍💻 Built For

**Amazon Nova AI Hackathon** — Demonstrating the power of Amazon Nova models for real-world startup tooling.

---

## 📝 License

MIT License — Built with ❤️ and Amazon Nova AI
