## Windows Setup (Dev Environment)

### Prerequisites
- Python 3.11+ from Microsoft Store or python.org (ensure "Add to PATH")
- Node.js 18+ from `https://nodejs.org`
- Git from `https://git-scm.com`

### Clone Repo
```
git clone <your-repo-url> finance_Agent
cd finance_Agent
cp .env.example .env
```

### Python Virtualenv
```
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

If PowerShell blocks script execution, run (once as Admin):
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Install Script Dependencies
```
pip install -r scripts/requirements.txt
```

### Run API Checks
```
python scripts/fetch_worldbank_inflation.py
python scripts/fetch_yahoo_indices.py
```

You should see basic JSON outputs verifying the endpoints are reachable. If these fail, the scripts fall back to defaults and print a warning.


