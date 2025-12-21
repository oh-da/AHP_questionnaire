# AHP Questionnaire Application

A modern, simplified AHP (Analytic Hierarchy Process) questionnaire application built with **SOLID principles**.

## 🚀 Getting Started

**New to this project?** Choose your guide:

- 📘 **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete step-by-step guide for beginners (A to Z)
- ⚡ **[QUICK_START.md](QUICK_START.md)** - 5-minute setup for experienced developers
- 🎨 **[VISUAL_GUIDE.md](VISUAL_GUIDE.md)** - Visual walkthrough with diagrams
- 📊 **[INSTALLATION_FLOWCHART.md](INSTALLATION_FLOWCHART.md)** - Flowchart-based setup guide
- 🚀 **[DEPLOYMENT_GUIDE_BEGINNERS.md](DEPLOYMENT_GUIDE_BEGINNERS.md)** - Deploy to Vercel & Railway
- 📇 **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Complete documentation index
- 📚 **Below** - Full documentation and architecture details

## 🎯 Features

- **Modern React Frontend** with TailwindCSS
- **SOLID-based Backend** with Flask
- **GitHub Gist Integration** for permanent result storage
- **Clean Architecture** with dependency injection
- **Type-safe** data models and interfaces

## 🏗️ Architecture

### Backend (SOLID Principles)

```
backend/
├── models.py           # Domain models (Data structures)
├── interfaces.py       # Abstract base classes (Contracts)
├── ahp_calculator.py   # AHP calculation logic
├── persistence.py      # GitHub Gist + In-memory storage
├── criteria_loader.py  # Criteria loading service
├── services.py         # Business logic orchestration
├── api.py              # Flask HTTP API
└── main.py             # Application entry point (DI)
```

**SOLID Principles Applied:**

1. **Single Responsibility**: Each class has one clear purpose
   - `AHPCalculator`: Pure calculation logic
   - `GitHubGistPersistence`: Data storage only
   - `AHPQuestionnaireAPI`: HTTP routing only

2. **Open/Closed**: Extend without modifying
   - New calculators can implement `IAHPCalculator`
   - New storage backends can implement `IPersistenceService`

3. **Liskov Substitution**: Interfaces are interchangeable
   - `GitHubGistPersistence` ↔ `InMemoryPersistence`
   - Both implement `IPersistenceService`

4. **Interface Segregation**: Focused interfaces
   - `IAHPCalculator`: Only calculation methods
   - `IPersistenceService`: Only persistence methods
   - `ICriteriaLoader`: Only loading methods

5. **Dependency Inversion**: Depend on abstractions
   - `AHPQuestionnaireService` depends on interfaces
   - Concrete implementations injected at runtime

### Frontend

```
frontend/
├── src/
│   ├── components/     # React components
│   ├── pages/          # Page components
│   ├── api/            # API client
│   └── utils/          # Utilities
└── ...
```

## 🚀 Quick Start

### Backend

```bash
# Install dependencies
pip install -r requirements-backend.txt

# Set up GitHub Gist (optional)
export GITHUB_TOKEN="your_github_token"
export GIST_ID="your_gist_id"  # Optional, will create new if not set

# Start server
python -m backend.main

# Or use the startup script
chmod +x start_backend.sh
./start_backend.sh
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Set API URL (optional)
echo "VITE_API_URL=http://localhost:5000" > .env

# Start development server
npm run dev

# Build for production
npm run build
```

## 🔧 Configuration

### Environment Variables

**Backend:**
- `GITHUB_TOKEN`: GitHub personal access token (for Gist storage)
- `GIST_ID`: Existing Gist ID (optional, creates new if not set)
- `GIST_FILENAME`: Filename in Gist (default: `ahp_results.csv`)
- `PORT`: Server port (default: `5000`)

**Frontend:**
- `VITE_API_URL`: Backend API URL (default: `http://localhost:5000`)

### Criteria Configuration

Create `criteria.csv` in the root directory:

```csv
Criterion
Passenger Activity
Service & Modes
Location
Population & Jobs
Bus Terminal
```

## 📡 API Endpoints

- `GET /api/health` - Health check
- `GET /api/criteria` - Get questionnaire criteria
- `GET /api/results` - Get all saved results
- `POST /api/calculate` - Calculate AHP weights and save

## 🧪 Testing

```bash
# Backend tests
pytest backend/

# Frontend tests
cd frontend && npm test
```

## 📦 Deployment

**New to deployment?** Check our complete guide:
- 🚀 **[DEPLOYMENT_GUIDE_BEGINNERS.md](DEPLOYMENT_GUIDE_BEGINNERS.md)** - Step-by-step Vercel + Railway deployment

### Quick Reference

**Backend (Railway/Render/Heroku):**
1. Set environment variables: `GITHUB_TOKEN`, `GIST_ID`, `PORT`
2. Build: `pip install -r requirements-backend.txt`
3. Start: `python -m backend.main`

**Frontend (Vercel/Netlify):**
1. Root directory: `frontend`
2. Build command: `npm run build`
3. Output directory: `dist`
4. Environment variable: `VITE_API_URL` (your backend URL)

## 🔄 Migration from Old Code

The old monolithic files are deprecated:
- ❌ `app.py` (Streamlit) → Use React frontend
- ❌ `api_server.py` (Monolithic Flask) → Use `backend/` module

## 🤝 Contributing

Contributions welcome! The architecture makes it easy to:

- Add new calculators (implement `IAHPCalculator`)
- Add new storage backends (implement `IPersistenceService`)
- Extend without modifying existing code

## 📄 License

MIT License

---

Built with ❤️ using SOLID principles
