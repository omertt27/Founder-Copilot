# 📸 Screenshot & Demo Video Guide

This guide explains how to capture the screenshots and demo video for the Founder Copilot hackathon submission.

---

## Screenshots Needed

Save all screenshots to `docs/screenshots/` with exactly these filenames:

| Filename | What to capture |
|----------|----------------|
| `01-input-panel.png` | Full app with feature cards visible, model selector showing "Nova 2 Lite", empty input |
| `02-output-startup-plan.png` | Output panel showing a generated Startup Plan with token count, time, and Nova 2 badge |
| `03-demo-mode.png` | Yellow demo mode banner at the top + any output card showing "Demo" badge |
| `04-github-issues.png` | GitHub Issues output with numbered issues, priorities, and acceptance criteria visible |

---

## How to Run the App for Screenshots

```bash
# Terminal 1 — Backend (demo mode, no AWS needed)
cd backend
python run.py

# Terminal 2 — Frontend
cd frontend
npm run dev
# Opens at http://localhost:5173
```

---

## Screenshot Tips

- **Resolution:** 1280×800 minimum, 1440×900 preferred
- **Browser:** Chrome or Safari, zoom at 100%
- **Window:** Full browser window (not just the app area) for best context
- **Tool (macOS):** `Cmd+Shift+4` → drag to select area, or `Cmd+Shift+5` for full window

### Suggested prompts to use:
- **Startup Plan:** `AI-powered meeting assistant that records meetings, generates summaries, and creates action items`
- **GitHub Issues:** `SaaS tool for freelancers to track time, send invoices, and manage clients`
- **Pitch Deck:** `Personalized AI tutor that adapts to each student's learning style and pace`

---

## 🎬 Demo Video (2–3 min)

### Suggested flow:

1. **0:00–0:20** — Show README/GitHub repo, mention Nova 2 models, hackathon context
2. **0:20–0:45** — Open the app, show feature cards and model selector (Nova 2 Lite default)
3. **0:45–1:30** — Type a prompt, generate a **Startup Plan**, scroll through the output
4. **1:30–2:00** — Switch to **GitHub Issues**, generate, show numbered issues with priorities
5. **2:00–2:30** — Show **Demo Mode** (clear `.env` credentials or set `DEMO_MODE=true`, restart, generate)
6. **2:30–3:00** — Show the API docs at `http://localhost:8000/docs`, mention streaming SSE

### Recording tools (macOS):
- **QuickTime Player** → File → New Screen Recording (free, built-in)
- **Loom** (free tier) — easy sharing link
- **OBS Studio** (free) — best quality

### Save as:
- `docs/demo-video.mp4` (or link to YouTube/Loom in README)

---

## After Capturing

1. Drop the PNG files into `docs/screenshots/`
2. Update `README.md` if the screenshot filenames differ
3. For the video, either:
   - Commit `docs/demo-video.mp4` (if under 50MB), or
   - Upload to YouTube/Loom and add the link to README

```bash
# Commit and push
git add docs/
git commit -m "📸 Add screenshots and demo video"
git push
```
