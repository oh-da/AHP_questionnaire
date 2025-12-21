# Railway Configuration Files 🚂

This repository includes configuration files for automatic Railway deployment.

## 📁 Configuration Files

### runtime.txt
Specifies the Python version to use.

```
python-3.11.0
```

**Purpose:** Tells Railway to use Python 3.11.0 for building and running the app.

### railway.json
Main Railway configuration file.

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements-backend.txt"
  },
  "deploy": {
    "startCommand": "python -m backend.main",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Purpose:**
- Tells Railway to use Nixpacks builder
- Specifies build command (install dependencies)
- Specifies start command (run the app)
- Configures restart policy (auto-restart on failure, max 10 retries)

### nixpacks.toml
Nixpacks build configuration.

```toml
[build]
builder = "NIXPACKS"

[build.nixpacksPlan]
providers = ["python"]

[build.nixpacksPlan.phases.setup]
nixPkgs = ["python311", "pip"]

[build.nixpacksPlan.phases.install]
cmds = ["pip install -r requirements-backend.txt"]

[build.nixpacksPlan.phases.build]
cmds = ["echo 'Build complete'"]

[build.nixpacksPlan.start]
cmd = "python -m backend.main"
```

**Purpose:**
- Ensures Python 3.11 and pip are available
- Defines build phases (setup, install, build, start)
- Guarantees pip is in PATH during build

### Procfile
Process file for deployment platforms (Railway, Heroku, etc.).

```
web: python -m backend.main
```

**Purpose:**
- Simple one-line start command
- Compatible with multiple deployment platforms

## 🔧 How Railway Uses These Files

1. **Detect:** Railway reads these files when you deploy
2. **Build:**
   - Installs Python 3.11 (from runtime.txt)
   - Installs dependencies (from railway.json or Procfile)
3. **Run:**
   - Starts the app with specified command
   - Auto-restarts on failure (from railway.json)

## ⚠️ Common Issues

### "pip: not found"

**Cause:** Railway couldn't detect Python or pip is not in PATH.

**Fix:** These configuration files fix this! Make sure they're all committed:
```bash
git add runtime.txt railway.json nixpacks.toml Procfile
git commit -m "Add Railway configuration"
git push
```

### Build fails

**Check:**
1. All config files are in repository root
2. `requirements-backend.txt` exists
3. Files are committed and pushed to GitHub
4. Railway is connected to the correct branch

## 🎯 Which File Does What?

| File | Required? | Purpose | Used By |
|------|-----------|---------|---------|
| runtime.txt | Recommended | Python version | Railway, Heroku |
| railway.json | Recommended | Railway-specific config | Railway only |
| nixpacks.toml | Recommended | Build configuration | Railway (Nixpacks) |
| Procfile | Optional | Generic start command | Railway, Heroku, others |

**Best practice:** Include all files for maximum compatibility!

## 🚀 Deployment Without These Files

If these files are missing, you'll need to configure manually in Railway:

1. Go to service → Settings
2. Set Build Command: `pip install -r requirements-backend.txt`
3. Set Start Command: `python -m backend.main`

**But with these files:** Railway auto-configures everything! ✨

## 📚 Learn More

- Railway Docs: https://docs.railway.app/
- Nixpacks: https://nixpacks.com/
- Python Buildpacks: https://github.com/railwayapp/nixpacks/tree/main/src/providers/python

---

**TL;DR:** These files tell Railway how to build and run your Python app automatically. Keep them in your repository root!
