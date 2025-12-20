# Deploying React + Flask API to Production

This guide shows how to deploy the React frontend on Vercel with the Flask API backend for GitHub Gist saving.

## Architecture

- **Frontend (React)** → Vercel
- **Backend (Flask API)** → Railway/Render
- **Storage** → GitHub Gist (free, permanent)

## 🚀 Step 1: Deploy Flask API

### Option A: Railway (Recommended - Free Tier)

1. **Sign up at [railway.app](https://railway.app)**

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your `AHP_questionnaire` repository

3. **Configure Build**
   - Railway auto-detects Python
   - Root Directory: Leave empty (uses root)
   - Build Command: `pip install -r requirements-api.txt`
   - Start Command: `python api_server.py`

4. **Set Environment Variables**
   - Go to Variables tab
   - Add:
     ```
     GITHUB_TOKEN=ghp_your_token_here
     PORT=5000
     ```

5. **Deploy**
   - Click "Deploy"
   - Wait ~2 minutes
   - Get your API URL: `https://your-app.up.railway.app`

### Option B: Render (Alternative)

1. **Sign up at [render.com](https://render.com)**

2. **New Web Service**
   - Connect GitHub repo
   - Root Directory: Leave empty
   - Build Command: `pip install -r requirements-api.txt`
   - Start Command: `python api_server.py`

3. **Environment Variables**
   ```
   GITHUB_TOKEN=ghp_your_token_here
   ```

4. **Deploy** and get your URL

---

## 🌐 Step 2: Deploy React Frontend on Vercel

1. **Go to [vercel.com](https://vercel.com)**

2. **Import Project**
   - New → Import Git Repository
   - Select `AHP_questionnaire`
   - Root Directory: `frontend`
   - Framework: Vite (auto-detected)

3. **Configure Environment Variable**
   - Go to Environment Variables
   - Add:
     ```
     VITE_API_URL=https://your-railway-app.up.railway.app
     ```
   - Replace with your actual Railway/Render URL from Step 1

4. **Deploy**
   - Click Deploy
   - Wait ~60 seconds
   - Get your Vercel URL: `https://ahp-questionnaire.vercel.app`

---

## ✅ Step 3: Test the Integration

1. **Visit your Vercel URL**
   - Example: `https://ahp-questionnaire.vercel.app`

2. **Complete a questionnaire**

3. **Check Results Page**
   - You should see: "התוצאות נשמרו ב-GitHub Gist בהצלחה! 🎉"
   - This means it's working!

4. **Verify on GitHub Gist**
   - Go to [gist.github.com](https://gist.github.com)
   - Check your secret gists
   - Find `ahp_results.csv`
   - Your results should be there!

---

## 🔧 Troubleshooting

### Frontend shows "API לא זמין"

**Check 1: API URL is correct**
```bash
# In Vercel dashboard → Settings → Environment Variables
# Should be: https://your-api.railway.app (no trailing slash)
```

**Check 2: API is running**
- Visit `https://your-api.railway.app` in browser
- Should see 404 (that's OK - means server is running)
- Visit `https://your-api.railway.app/api/results`
- Should see `[]` or results array

**Check 3: CORS is enabled**
- API should allow requests from your Vercel domain
- Check Railway logs for CORS errors

### Results not saving to GitHub Gist

**Check Railway Logs:**
1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" → Latest → "View Logs"
4. Look for:
   - ✅ "Saved to GitHub Gist: ..." (success)
   - ⚠️ "GITHUB_TOKEN not set" (need to add env var)
   - ❌ "Error saving to Gist" (token invalid)

**Fix:**
- Make sure `GITHUB_TOKEN` is set in Railway environment variables
- Token must have 'gist' scope
- Generate new token if needed at: https://github.com/settings/tokens

### API works locally but not on Railway

**Common issues:**
1. Wrong requirements file - Use `requirements-api.txt` not `requirements.txt`
2. Port binding - Railway provides PORT env var automatically
3. Missing dependencies - Make sure pandas and requests are in requirements-api.txt

---

## 🎯 Quick Deployment Checklist

- [ ] Create GitHub personal access token with 'gist' scope
- [ ] Deploy Flask API on Railway
- [ ] Set GITHUB_TOKEN in Railway env vars
- [ ] Get Railway API URL
- [ ] Deploy React on Vercel
- [ ] Set VITE_API_URL in Vercel env vars
- [ ] Test questionnaire completion
- [ ] Verify results in GitHub Gist

---

## 💰 Cost

**Everything is FREE!**

- ✅ Railway Free Tier: 500 hours/month
- ✅ Vercel Free Tier: Unlimited
- ✅ GitHub Gist: Free unlimited private gists

Perfect for personal projects and moderate usage!

---

## 🔄 Local Development

For local testing with API:

```bash
# Terminal 1: Flask API
export GITHUB_TOKEN=ghp_your_token
python api_server.py

# Terminal 2: React Dev Server
cd frontend
VITE_API_URL=http://localhost:5000 npm run dev
```

Visit: http://localhost:3000

---

## 📊 Monitoring

**Check API Health:**
```bash
curl https://your-api.railway.app/api/results
```

**Check Logs:**
- Railway: Dashboard → Deployments → View Logs
- Vercel: Dashboard → Deployments → Function Logs

---

## 🎉 You're Done!

Now your React app on Vercel automatically saves all results to GitHub Gist via the Flask API!

**Architecture:**
```
User → Vercel (React) → Railway (Flask API) → GitHub Gist
```

Every questionnaire completion is permanently saved! 🚀
