# Installation Flowchart 📊

Visual guide to help you install and run the AHP Questionnaire application.

```
┌─────────────────────────────────────────────────────────────┐
│                    START HERE                                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Do you have Python, Node,   │
        │   and Git installed?          │
        └───────┬───────────────┬───────┘
                │ No            │ Yes
                │               │
                ▼               ▼
    ┌─────────────────┐   ┌─────────────────┐
    │ Install Software │   │  Skip to Step 2 │
    │                  │   └────────┬────────┘
    │ • Python 3.8+   │            │
    │ • Node.js 16+   │            │
    │ • Git           │            │
    │                  │            │
    │ See: GETTING_   │            │
    │ STARTED.md      │            │
    │ Step 1          │            │
    └────────┬────────┘            │
             │                      │
             └──────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │ Clone Repository      │
            │                       │
            │ git clone <repo_url>  │
            │ cd AHP_questionnaire  │
            └───────────┬───────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Want to save results to     │
        │   GitHub Gist? (Recommended)  │
        └───────┬───────────────┬───────┘
                │ Yes           │ No
                │               │
                ▼               │
    ┌─────────────────────┐    │
    │ Setup GitHub Gist   │    │
    │                     │    │
    │ 1. Create GitHub    │    │
    │    account          │    │
    │ 2. Generate token   │    │
    │    (gist scope)     │    │
    │ 3. Set env var:     │    │
    │    GITHUB_TOKEN     │    │
    │                     │    │
    │ See: GETTING_       │    │
    │ STARTED.md Step 3   │    │
    └──────────┬──────────┘    │
               │                │
               └────────┬───────┘
                        │
                        ▼
            ┌───────────────────────┐
            │ Install Backend       │
            │                       │
            │ pip install -r        │
            │ requirements-         │
            │ backend.txt           │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │ Install Frontend      │
            │                       │
            │ cd frontend           │
            │ npm install           │
            │ cd ..                 │
            └───────────┬───────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   Open TWO terminal windows   │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────┬───────────────┐
        │               │               │
        ▼               ▼               │
┌──────────────┐  ┌──────────────┐    │
│ Terminal 1   │  │ Terminal 2   │    │
│ (Backend)    │  │ (Frontend)   │    │
│              │  │              │    │
│ python -m    │  │ cd frontend  │    │
│ backend.main │  │ npm run dev  │    │
│              │  │              │    │
│ Keep open!   │  │ Keep open!   │    │
└──────┬───────┘  └──────┬───────┘    │
       │                  │             │
       └────────┬─────────┘             │
                │                       │
                ▼                       │
    ┌───────────────────────┐          │
    │ Backend should show:  │          │
    │ ✓ Server starting on  │          │
    │   port 5000           │          │
    └───────────┬───────────┘          │
                │                       │
                ▼                       │
    ┌───────────────────────┐          │
    │ Frontend should show: │          │
    │ Local:                │          │
    │ http://localhost:5173/│          │
    └───────────┬───────────┘          │
                │                       │
                ▼                       │
        ┌───────────────┐              │
        │ Open Browser  │              │
        │               │              │
        │ Visit:        │              │
        │ localhost:5173│              │
        └───────┬───────┘              │
                │                       │
                ▼                       │
        ┌───────────────┐              │
        │   SUCCESS!    │              │
        │      🎉       │              │
        │               │              │
        │ Start using   │              │
        │ the app!      │              │
        └───────────────┘              │
                                        │
                                        ▼
                            ┌───────────────────┐
                            │  Having issues?   │
                            │                   │
                            │  Check:           │
                            │  • GETTING_       │
                            │    STARTED.md     │
                            │    Troubleshooting│
                            │  • Both terminals │
                            │    are running    │
                            │  • No firewall    │
                            │    blocking       │
                            └───────────────────┘
```

## Quick Reference Commands

### First Time Setup
```bash
# 1. Clone
git clone https://github.com/oh-da/AHP_questionnaire.git
cd AHP_questionnaire

# 2. Install backend
pip install -r requirements-backend.txt

# 3. Install frontend
cd frontend && npm install && cd ..

# 4. (Optional) Set GitHub token
export GITHUB_TOKEN=ghp_your_token_here  # macOS/Linux
set GITHUB_TOKEN=ghp_your_token_here     # Windows
```

### Every Time You Run
```bash
# Terminal 1 - Backend
python -m backend.main

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### Access
- **Frontend:** http://localhost:5173/
- **Backend API:** http://localhost:5000/api/health

## Troubleshooting Quick Fixes

| Issue | Command |
|-------|---------|
| Python not found | Try `python3` or `py` |
| Port 5000 in use | `PORT=3000 python -m backend.main` |
| Module not found | `pip install -r requirements-backend.txt` |
| Frontend can't connect | Check backend is running on port 5000 |

## Need More Help?

📘 **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed installation guide

⚡ **[QUICK_START.md](QUICK_START.md)** - Fast setup for pros

🔧 **[README.md](README.md)** - Full documentation
