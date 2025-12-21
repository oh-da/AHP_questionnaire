# Visual Setup Guide 🎨

Step-by-step visual walkthrough of the installation process.

---

## 📦 Step 1: Install Software

```
┌─────────────────────────────────────────┐
│  Your Computer (Empty)                  │
│                                         │
│  ❌ No Python                           │
│  ❌ No Node.js                          │
│  ❌ No Git                              │
└─────────────────────────────────────────┘
                  │
                  │ Install...
                  ▼
┌─────────────────────────────────────────┐
│  Your Computer (Ready!)                 │
│                                         │
│  ✅ Python 3.11                         │
│  ✅ Node.js 18                          │
│  ✅ Git                                 │
└─────────────────────────────────────────┘
```

**How:**
- Python: https://python.org/downloads
- Node.js: https://nodejs.org
- Git: https://git-scm.com

---

## 📥 Step 2: Download Project

```
┌─────────────────────┐
│   GitHub Cloud      │
│                     │
│  AHP_questionnaire  │
│  Repository         │
└──────────┬──────────┘
           │
           │ git clone
           │
           ▼
┌─────────────────────┐
│  Your Computer      │
│                     │
│  📁 AHP_questionnaire/
│    ├── backend/     │
│    ├── frontend/    │
│    └── ...          │
└─────────────────────┘
```

**Command:**
```bash
git clone https://github.com/oh-da/AHP_questionnaire.git
cd AHP_questionnaire
```

---

## 🔑 Step 3: GitHub Gist Setup (Optional)

```
┌──────────────────────────────────────────────┐
│  GitHub Website                              │
│                                              │
│  Settings → Developer Settings →            │
│  Personal Access Tokens                      │
│                                              │
│  ┌────────────────────────────────┐         │
│  │ Token Name: AHP Questionnaire  │         │
│  │ Scopes: [✓] gist              │         │
│  │                                │         │
│  │ [Generate Token]               │         │
│  └────────────────────────────────┘         │
│                                              │
│  Your Token: ghp_xxxxxxxxxxxx (COPY THIS!)  │
└──────────────────────────────────────────────┘
                    │
                    │ Set as environment variable
                    ▼
┌──────────────────────────────────────────────┐
│  Your Terminal                               │
│                                              │
│  $ export GITHUB_TOKEN=ghp_xxxxxxxxxxxx     │
│                                              │
│  ✅ Token saved                              │
└──────────────────────────────────────────────┘
```

---

## 📦 Step 4: Install Dependencies

### Backend

```
┌─────────────────────────────┐
│  requirements-backend.txt   │
│                             │
│  • flask                    │
│  • flask-cors               │
│  • numpy                    │
│  • pandas                   │
│  • requests                 │
└──────────┬──────────────────┘
           │
           │ pip install -r requirements-backend.txt
           ▼
┌─────────────────────────────┐
│  Python Environment         │
│                             │
│  ✅ All packages installed  │
│  ✅ Ready to run backend    │
└─────────────────────────────┘
```

### Frontend

```
┌─────────────────────────────┐
│  frontend/package.json      │
│                             │
│  • react                    │
│  • vite                     │
│  • tailwindcss              │
│  • (100+ more packages)     │
└──────────┬──────────────────┘
           │
           │ npm install (takes 2-5 min)
           ▼
┌─────────────────────────────┐
│  frontend/node_modules/     │
│                             │
│  ✅ All packages installed  │
│  ✅ Ready to run frontend   │
└─────────────────────────────┘
```

---

## 🚀 Step 5: Start Both Servers

### Two Terminals Side by Side

```
┌─────────────────────────┐  ┌─────────────────────────┐
│   Terminal 1 (Backend)  │  │  Terminal 2 (Frontend)  │
├─────────────────────────┤  ├─────────────────────────┤
│                         │  │                         │
│ $ python -m backend.main│  │ $ cd frontend           │
│                         │  │ $ npm run dev           │
│ ✓ Server starting...    │  │                         │
│ ✓ Port 5000             │  │ ✓ Vite dev server...    │
│ ✓ GitHub Gist OK        │  │ ✓ Port 5173             │
│                         │  │                         │
│ [Keep this running! →]  │  │ [Keep this running! →]  │
│                         │  │                         │
└─────────────────────────┘  └─────────────────────────┘
          │                            │
          │                            │
          └──────────┬─────────────────┘
                     │
                     ▼
           ┌─────────────────┐
           │  Both Running!  │
           └─────────────────┘
```

**Important:** Don't close either terminal!

---

## 🌐 Step 6: Open Browser

```
┌────────────────────────────────────────────┐
│  Your Web Browser                          │
│  ┌──────────────────────────────────────┐ │
│  │ http://localhost:5173                 │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │                                      │ │
│  │         📊 שאלון AHP                 │ │
│  │                                      │ │
│  │  Welcome! This questionnaire...      │ │
│  │                                      │ │
│  │  ┌────────────────────────────────┐ │ │
│  │  │ שמך (אופציונלי)                │ │ │
│  │  │ [Ohad Dahan____________]        │ │ │
│  │  └────────────────────────────────┘ │ │
│  │                                      │ │
│  │  Criteria: Passenger Activity...     │ │
│  │                                      │ │
│  │  [התחל] ←── Click here to start    │ │
│  │                                      │ │
│  └──────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

---

## 🎯 Step 7: Use the Application

### Questionnaire Flow

```
┌─────────────────────────────────────────────┐
│  Question 1 of 10                           │
│  ━━━━━━━━━━░░░░░░░░░░░░░░░░░░ 10%         │
│                                             │
│  Which is more important?                   │
│                                             │
│  ┌─────────────────┐ vs ┌─────────────────┐│
│  │ Passenger       │    │ Service & Modes ││
│  │ Activity        │    │                 ││
│  └─────────────────┘    └─────────────────┘│
│                                             │
│  ←─────────●─────────→                     │
│  More       Equal    More                   │
│  important           important              │
│                                             │
│  [Previous]              [Next →]           │
└─────────────────────────────────────────────┘
         │
         │ Answer all questions
         ▼
┌─────────────────────────────────────────────┐
│  ✅ Results                                 │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ Consistency: ✓ PASS (CR = 0.05)    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  Priority Weights:                          │
│  ┌─────────────────────────────────────┐   │
│  │ Passenger Activity  ████████ 35%   │   │
│  │ Location           ██████ 25%      │   │
│  │ Service & Modes    ████ 20%        │   │
│  │ Population & Jobs  ███ 15%         │   │
│  │ Bus Terminal       █ 5%            │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ✅ Saved to GitHub Gist!                  │
│                                             │
│  [Download Results]  [New Questionnaire]    │
└─────────────────────────────────────────────┘
```

---

## 💾 Behind the Scenes: Data Flow

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │
       │ HTTP POST /api/calculate
       │ { userName, criteria, comparisons }
       ▼
┌─────────────────────────┐
│   Backend Server        │
│   (Flask API)           │
├─────────────────────────┤
│ 1. Receive request      │
│ 2. Calculate AHP        │ ← AHPCalculator
│ 3. Save to Gist         │ ← GitHubGistPersistence
│ 4. Return results       │
└──────┬──────────────────┘
       │
       │ Results + Save Status
       ▼
┌──────────────────────────┐
│   GitHub Gist            │
│   (Cloud Storage)        │
├──────────────────────────┤
│ ahp_results.csv          │
│                          │
│ timestamp,user_name,...  │
│ 2024-01-...,Ohad,...    │
│ 2024-01-...,Sarah,...   │
│                          │
│ ✅ Saved permanently!    │
└──────────────────────────┘
       │
       │ (Viewable at gist.github.com)
       ▼
┌──────────────────────────┐
│   You can view online!   │
└──────────────────────────┘
```

---

## 🔄 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Your Computer                        │
│                                                         │
│  ┌───────────────┐          ┌────────────────┐         │
│  │   Backend     │          │   Frontend     │         │
│  │   :5000       │ ←──────→ │   :5173        │         │
│  │               │   API    │                │         │
│  │  ┌─────────┐  │          │  React + Vite  │         │
│  │  │ Flask   │  │          │  TailwindCSS   │         │
│  │  │ API     │  │          └────────┬───────┘         │
│  │  └────┬────┘  │                   │                 │
│  │       │       │                   │                 │
│  │  ┌────▼────┐  │                   │                 │
│  │  │Services │  │                   │                 │
│  │  └────┬────┘  │            Your Browser             │
│  │       │       │            shows this               │
│  │  ┌────▼──────────────┐                              │
│  │  │ AHP Calculator    │                              │
│  │  │ Persistence       │                              │
│  │  │ Criteria Loader   │                              │
│  │  └────┬──────────────┘                              │
│  └───────┼────────────────┘                            │
│          │                                             │
└──────────┼─────────────────────────────────────────────┘
           │
           │ HTTPS
           │
           ▼
┌──────────────────────┐
│   GitHub.com         │
│   (Internet)         │
│                      │
│  Your Gist:          │
│  ahp_results.csv     │
│                      │
│  ✅ Free Storage     │
│  ✅ Always Online    │
│  ✅ Version History  │
└──────────────────────┘
```

---

## 🎬 Complete Setup Animation

```
Frame 1: Empty computer
  💻

Frame 2: Installing software...
  💻 ⚙️ Installing Python...

Frame 3: Software installed!
  💻 ✅ Python ✅ Node ✅ Git

Frame 4: Cloning repository...
  💻 📦 git clone...

Frame 5: Repository cloned!
  💻 📁 AHP_questionnaire/

Frame 6: Installing dependencies...
  💻 ⚙️ pip install...
     ⚙️ npm install...

Frame 7: Dependencies installed!
  💻 ✅ Backend ready
     ✅ Frontend ready

Frame 8: Starting servers...
  💻 🚀 Backend starting...
     🚀 Frontend starting...

Frame 9: Servers running!
  💻 ✅ Backend :5000
     ✅ Frontend :5173

Frame 10: Opening browser...
  💻 🌐 localhost:5173

Frame 11: SUCCESS!
  💻 🎉 Application running!
     📊 Questionnaire ready!

Frame 12: Using the app...
  💻 👤 User answering questions
     📊 Calculating results
     💾 Saving to GitHub Gist

Frame 13: Results saved!
  💻 ✅ Results calculated
     ☁️ Saved to cloud
     🎊 Done!
```

---

## ✅ Success Checklist

Use this to verify everything is working:

```
Installation Checklist:
  [ ] Python installed (python --version works)
  [ ] Node.js installed (node --version works)
  [ ] Git installed (git --version works)
  [ ] Repository cloned (folder exists)
  [ ] Backend dependencies installed (no errors)
  [ ] Frontend dependencies installed (no errors)

Running Checklist:
  [ ] Backend terminal open and running
  [ ] Frontend terminal open and running
  [ ] Backend shows "Server starting on port 5000"
  [ ] Frontend shows "Local: http://localhost:5173"
  [ ] Browser can open localhost:5173
  [ ] Can see the questionnaire page

GitHub Gist (Optional):
  [ ] GitHub account created
  [ ] Personal access token created
  [ ] Token has 'gist' permission
  [ ] GITHUB_TOKEN environment variable set
  [ ] Backend shows "GitHub Gist persistence configured"

Usage Checklist:
  [ ] Can enter name
  [ ] Can see criteria
  [ ] Can start questionnaire
  [ ] Can answer questions with slider
  [ ] Can navigate (Previous/Next)
  [ ] Can finish questionnaire
  [ ] Can see results
  [ ] Results show consistency check
  [ ] Results show weights chart
  [ ] Can download results
  [ ] (If Gist) Results saved to GitHub
```

---

## 🆘 Quick Help

**Something not working?**

1. ✅ **Check both terminals are running**
   - Backend should show "Server starting..."
   - Frontend should show "Local: http://localhost:5173"

2. ✅ **Try restarting everything**
   - Press Ctrl+C in both terminals
   - Start backend again: `python -m backend.main`
   - Start frontend again: `cd frontend && npm run dev`

3. ✅ **Check the detailed guides**
   - [GETTING_STARTED.md](GETTING_STARTED.md) - Full troubleshooting
   - [QUICK_START.md](QUICK_START.md) - Quick reference

4. ✅ **Still stuck?**
   - Check [INSTALLATION_FLOWCHART.md](INSTALLATION_FLOWCHART.md)
   - Open an issue on GitHub

---

**You've got this!** 💪

The hardest part is just getting started. Once everything is installed, it's easy to run again and again!
