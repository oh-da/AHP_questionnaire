# Quick Start Guide ⚡

**Too long, didn't read?** Here's the fastest way to get started!

## Prerequisites

Install these first:
- Python 3.8+ → https://www.python.org/downloads/
- Node.js 16+ → https://nodejs.org/
- Git → https://git-scm.com/

## 5-Minute Setup

```bash
# 1. Clone the repository
git clone https://github.com/oh-da/AHP_questionnaire.git
cd AHP_questionnaire

# 2. Install backend dependencies
pip install -r requirements-backend.txt

# 3. Install frontend dependencies
cd frontend
npm install
cd ..

# 4. Start backend (Terminal 1)
python -m backend.main

# 5. Start frontend (Terminal 2 - open a new one!)
cd frontend
npm run dev
```

## Open Your Browser

Go to: **http://localhost:5173/**

That's it! 🎉

---

## Optional: GitHub Gist Setup

To save results permanently:

1. **Get GitHub Token:**
   - GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - Check only: `gist`
   - Copy token (starts with `ghp_...`)

2. **Set environment variable:**
   ```bash
   # macOS/Linux
   export GITHUB_TOKEN=ghp_your_token_here

   # Windows
   set GITHUB_TOKEN=ghp_your_token_here
   ```

3. **Restart backend**

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "python not found" | Try `py` or `python3` |
| "npm not found" | Install Node.js and restart terminal |
| Port 5000 in use | `PORT=3000 python -m backend.main` |
| Can't connect | Make sure backend is running |

---

## Need More Help?

Read the complete guide: **GETTING_STARTED.md**

Or check: **README.md** for full documentation
