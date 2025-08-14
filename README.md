## Finance Agent

An AI-assisted personal finance planner for Indian users. It parses natural-language goals (e.g., "Plan my wedding in December 2026 for ₹8 lakhs"), calculates inflation-adjusted future costs and monthly savings needs, and surfaces simple investment recommendations. Built for a fast hackathon sprint.

### Tech Stack
- **Backend**: FastAPI, SQLite, spaCy + regex
- **Frontend**: React (Vite), Tailwind CSS, Chart.js, Lucide React
- **Integrations**: World Bank (inflation), Yahoo Finance (Nifty/Sensex)
- **DevOps**: Railway (backend), Vercel (frontend)

### Monorepo Structure
```
finance_Agent/
  backend/                 # FastAPI app (Uday)
  frontend/                # React + Vite app (Swastika)
  scripts/                 # One-off utilities for APIs and data (Mohit)
  docs/                    # Setup, API notes, ADRs
  .github/                 # (optional) Issue/PR templates, CI
  .env.example             # Shared env vars template
  .editorconfig            # Consistent formatting across editors
  .gitignore
  README.md
```

### Quickstart (Local)
This repo is set up so each area can move independently from Day 1.

1) Prereqs
- Python 3.11+
- Node 18+ (or 20+)
- Git

2) Clone and bootstrap
```
git clone <your-repo-url> finance_Agent
cd finance_Agent
cp .env.example .env
```

3) Backend (FastAPI) – placeholder until backend is added
```
cd backend
# Create venv and install once backend is scaffolded
```

4) Frontend (Vite) – placeholder until frontend is added
```
cd frontend
# Install deps once frontend is scaffolded
```

5) Utility scripts (API sanity checks)
```
python -m venv .venv
./.venv/Scripts/Activate.ps1  # Windows PowerShell
pip install -r scripts/requirements.txt
python scripts/fetch_worldbank_inflation.py
python scripts/fetch_yahoo_indices.py
```

### Environment Variables
Copy `.env.example` to `.env` and adjust as needed. For Day 1, Yahoo Finance endpoints used here do not require keys. If you choose a RapidAPI or other provider, add keys accordingly.

### Day 1 Objectives (Mohit)
- GitHub repo and baseline documentation
- Development environment setup notes (Windows-friendly)
- Research and verify World Bank + Yahoo Finance endpoints with scripts
- Add core project configuration files

### License
MIT (adjust as needed)


