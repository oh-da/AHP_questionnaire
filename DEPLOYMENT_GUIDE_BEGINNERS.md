# Deployment Guide for Beginners 🚀

Complete step-by-step guide to deploy your AHP Questionnaire application online using **Vercel** (frontend) and **Railway** (backend).

**Why deploy?**
- ✅ Access from anywhere (not just localhost)
- ✅ Share with others via a URL
- ✅ Professional deployment
- ✅ Both services have **FREE tiers**!

---

## 📋 What You'll Need

Before starting:
- [x] GitHub account
- [x] Your code pushed to GitHub repository
- [x] GitHub Personal Access Token (for Gist storage)
- [x] 30-45 minutes of time

**Cost:** FREE! Both Vercel and Railway offer generous free tiers.

---

## 🎯 Overview: What We're Deploying

```
┌─────────────────────────────────────────────┐
│           Users Access Via Browser          │
│         https://your-app.vercel.app         │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│            Vercel (Frontend)                │
│         React + Vite + TailwindCSS          │
│              Static Files                    │
└─────────────────┬───────────────────────────┘
                  │
                  │ API Calls
                  ▼
┌─────────────────────────────────────────────┐
│          Railway (Backend)                  │
│         Python Flask API Server             │
│      https://your-backend.railway.app       │
└─────────────────┬───────────────────────────┘
                  │
                  │ Save Results
                  ▼
┌─────────────────────────────────────────────┐
│           GitHub Gist                       │
│        Permanent CSV Storage                │
└─────────────────────────────────────────────┘
```

---

## 📦 Part 1: Deploy Backend to Railway

Railway will host your Python backend server.

### Step 1.1: Create Railway Account

1. **Go to:** https://railway.app/
2. **Click:** "Start a New Project" or "Login"
3. **Sign up with GitHub:**
   - Click "Login with GitHub"
   - Authorize Railway to access your GitHub
   - ✅ You're now logged in!

### Step 1.2: Create New Project

1. **Click:** "New Project" (big purple button)
2. **Select:** "Deploy from GitHub repo"
3. **Choose your repository:**
   - Find: `AHP_questionnaire`
   - Click on it
4. **Railway will detect your project** ⏳ (takes a few seconds)

### Step 1.3: Configure the Service

Once the project is created:

1. **Click on the service** (should show your repo name)
2. **Go to "Settings" tab**
3. **Configure:**

   **Root Directory:**
   - Leave empty (we're at the root)

   **Build Command:**
   - Click "Custom Build Command"
   - Enter: `pip install -r requirements-backend.txt`

   **Start Command:**
   - Click "Custom Start Command"
   - Enter: `python -m backend.main`

4. **Click "Deploy"** at the top right

### Step 1.4: Add Environment Variables

This is **CRITICAL** for GitHub Gist to work!

1. **Go to "Variables" tab**
2. **Click "New Variable"**
3. **Add these variables:**

   **Variable 1:**
   - Name: `GITHUB_TOKEN`
   - Value: `ghp_your_token_here` (your GitHub token)
   - Click "Add"

   **Variable 2:**
   - Name: `GIST_ID`
   - Value: `your_gist_id_here` (your Gist ID - optional)
   - Click "Add"

   **Variable 3:**
   - Name: `PORT`
   - Value: `5000`
   - Click "Add"

4. **Railway will automatically redeploy** after adding variables

### Step 1.5: Get Your Backend URL

1. **Go to "Settings" tab**
2. **Scroll to "Networking" section**
3. **Click "Generate Domain"**
4. **Copy the URL** - it looks like:
   ```
   https://your-app-production-xxxx.up.railway.app
   ```
5. **Save this URL!** You'll need it for the frontend.

### Step 1.6: Test Your Backend

1. **Open your backend URL in browser:**
   ```
   https://your-backend.railway.app/api/health
   ```

2. **You should see:**
   ```json
   {
     "status": "ok",
     "criteriaCount": 5,
     "gistConfigured": true
   }
   ```

3. ✅ **Backend is working!**

---

## 🎨 Part 2: Deploy Frontend to Vercel

Vercel will host your React frontend.

### Step 2.1: Create Vercel Account

1. **Go to:** https://vercel.com/
2. **Click:** "Sign Up"
3. **Sign up with GitHub:**
   - Click "Continue with GitHub"
   - Authorize Vercel
   - ✅ You're logged in!

### Step 2.2: Import Your Project

1. **Click:** "Add New..." → "Project"
2. **Find your repository:**
   - Look for: `AHP_questionnaire`
   - Click "Import"

### Step 2.3: Configure Project

**Important settings:**

1. **Project Name:**
   - Use: `ahp-questionnaire` (or your preferred name)

2. **Framework Preset:**
   - Select: "Vite"

3. **Root Directory:**
   - Click "Edit"
   - Enter: `frontend`
   - ✅ This is critical! Tells Vercel where the frontend code is.

4. **Build Command:**
   - Should auto-fill: `npm run build`
   - If not, enter it manually

5. **Output Directory:**
   - Should auto-fill: `dist`
   - If not, enter it manually

6. **Install Command:**
   - Should auto-fill: `npm install`

### Step 2.4: Add Environment Variables

**CRITICAL:** Tell the frontend where your backend is!

1. **Before clicking Deploy, expand "Environment Variables"**
2. **Add variable:**
   - Name: `VITE_API_URL`
   - Value: `https://your-backend.railway.app` (your Railway URL from Part 1)
   - ⚠️ **Remove trailing slash** if any!
   - Click "Add"

### Step 2.5: Deploy!

1. **Click:** "Deploy"
2. **Wait 1-3 minutes** ⏳
   - Vercel will:
     - Install dependencies
     - Build your React app
     - Deploy it
3. **You'll see:** "Congratulations! 🎉"

### Step 2.6: Get Your Frontend URL

1. **Vercel will show your URL:**
   ```
   https://ahp-questionnaire.vercel.app
   ```
2. **Click "Visit"** to open your app!

### Step 2.7: Test Your Application

1. **Open:** `https://your-app.vercel.app`
2. **You should see:** The AHP Questionnaire interface
3. **Test it:**
   - Enter your name
   - Start the questionnaire
   - Answer some questions
   - Check if results save to GitHub Gist
4. ✅ **Fully deployed and working!**

---

## 🔧 Common Issues & Solutions

### Backend Issues

#### Issue: "Application failed to respond"

**Solution:**
1. Check Railway logs (click service → "Deployments" → latest → "View Logs")
2. Look for errors
3. Common fixes:
   - Verify `requirements-backend.txt` exists
   - Check start command: `python -m backend.main`
   - Ensure PORT=5000 is set

#### Issue: "Module not found"

**Solution:**
1. Check build command includes: `pip install -r requirements-backend.txt`
2. Redeploy: Go to "Deployments" → click "..." → "Redeploy"

#### Issue: Results not saving to Gist

**Solution:**
1. Verify `GITHUB_TOKEN` is set correctly in Railway variables
2. Token must have `gist` permission
3. Check logs for GitHub API errors

### Frontend Issues

#### Issue: "Can't connect to backend"

**Solution:**
1. Check `VITE_API_URL` environment variable
2. Should be: `https://your-backend.railway.app` (no trailing slash)
3. Redeploy after changing environment variables

#### Issue: "404 Not Found"

**Solution:**
1. Verify Root Directory is set to: `frontend`
2. Verify Output Directory is: `dist`
3. Redeploy the project

#### Issue: Build fails with "command not found"

**Solution:**
1. Check Framework Preset is set to "Vite"
2. Verify Build Command: `npm run build`
3. Check Install Command: `npm install`

---

## 🔄 How to Update Your Deployment

When you make code changes:

### Update Backend (Railway)

1. **Push changes to GitHub:**
   ```bash
   git add .
   git commit -m "Update backend"
   git push
   ```

2. **Railway auto-deploys!**
   - Check "Deployments" tab to see progress
   - Usually takes 1-2 minutes

### Update Frontend (Vercel)

1. **Push changes to GitHub:**
   ```bash
   git add .
   git commit -m "Update frontend"
   git push
   ```

2. **Vercel auto-deploys!**
   - Check Vercel dashboard for progress
   - Usually takes 1-3 minutes

---

## 💰 Free Tier Limits

### Railway Free Tier

- ✅ $5 credit per month (usually enough!)
- ✅ Sleeps after inactivity (wakes up automatically)
- ✅ 500 hours per month
- ✅ Shared CPU

**For this project:** Should be well within free tier!

### Vercel Free Tier

- ✅ Unlimited static deployments
- ✅ 100 GB bandwidth per month
- ✅ Custom domains
- ✅ Automatic HTTPS

**For this project:** Perfect for free tier!

---

## 🌐 Custom Domain (Optional)

### Add Custom Domain to Vercel

1. **Buy a domain** (from Namecheap, GoDaddy, etc.)
2. **In Vercel:**
   - Go to project → "Settings" → "Domains"
   - Click "Add"
   - Enter your domain: `questionnaire.yourdomain.com`
3. **In your domain registrar:**
   - Add CNAME record:
     - Name: `questionnaire`
     - Value: `cname.vercel-dns.com`
4. **Wait 5-10 minutes** for DNS to propagate
5. ✅ **Your app is now at your custom domain!**

---

## 📊 Monitoring Your Deployment

### Railway Monitoring

1. **Go to your project**
2. **Click "Observability"**
3. **See:**
   - CPU usage
   - Memory usage
   - Request logs
   - Error logs

### Vercel Monitoring

1. **Go to your project**
2. **Click "Analytics"** (may need to enable)
3. **See:**
   - Page views
   - Performance metrics
   - Geographic distribution

---

## 🔐 Security Best Practices

### Environment Variables

✅ **DO:**
- Store tokens in environment variables
- Never commit `.env` files
- Regenerate tokens if exposed

❌ **DON'T:**
- Hardcode tokens in code
- Share tokens publicly
- Commit secrets to GitHub

### GitHub Token

- ✅ Use minimal permissions (only `gist`)
- ✅ Set expiration date
- ✅ Regenerate periodically

---

## 📝 Deployment Checklist

### Before Deployment

- [ ] Code works locally (tested on localhost)
- [ ] All changes committed to GitHub
- [ ] GitHub token ready (with `gist` permission)
- [ ] Gist ID ready (optional)
- [ ] Repository is public or Vercel/Railway has access

### Backend Deployment (Railway)

- [ ] Railway account created
- [ ] Project created from GitHub repo
- [ ] Build command set: `pip install -r requirements-backend.txt`
- [ ] Start command set: `python -m backend.main`
- [ ] `GITHUB_TOKEN` environment variable set
- [ ] `GIST_ID` environment variable set (optional)
- [ ] `PORT` environment variable set to `5000`
- [ ] Domain generated
- [ ] Health endpoint tested (`/api/health`)

### Frontend Deployment (Vercel)

- [ ] Vercel account created
- [ ] Project imported from GitHub
- [ ] Root directory set to: `frontend`
- [ ] Framework preset: Vite
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist`
- [ ] `VITE_API_URL` environment variable set (Railway URL)
- [ ] Deployment successful
- [ ] App tested in browser
- [ ] Backend connection works
- [ ] Results save to Gist

### Post-Deployment

- [ ] Full questionnaire flow tested
- [ ] Results visible in GitHub Gist
- [ ] No console errors in browser
- [ ] Mobile responsive (test on phone)
- [ ] Shared URL with others (optional)

---

## 🎬 Quick Visual Guide

### Railway Deployment Flow

```
Step 1: Create Account
  🌐 railway.app → Sign up with GitHub

Step 2: New Project
  ➕ New Project → Deploy from GitHub repo

Step 3: Select Repo
  📁 Choose: AHP_questionnaire

Step 4: Configure
  ⚙️ Settings → Custom Start Command
  💻 python -m backend.main

Step 5: Environment Variables
  🔐 Variables → Add:
     GITHUB_TOKEN=ghp_...
     GIST_ID=...
     PORT=5000

Step 6: Generate Domain
  🌐 Settings → Networking → Generate Domain

Step 7: Test
  ✅ Visit: https://your-app.railway.app/api/health
```

### Vercel Deployment Flow

```
Step 1: Create Account
  🌐 vercel.com → Sign up with GitHub

Step 2: New Project
  ➕ Add New → Project

Step 3: Import Repo
  📁 Choose: AHP_questionnaire → Import

Step 4: Configure
  📂 Root Directory: frontend
  ⚡ Framework: Vite
  📦 Build: npm run build
  📁 Output: dist

Step 5: Environment Variable
  🔐 Add: VITE_API_URL=https://your-backend.railway.app

Step 6: Deploy
  🚀 Click: Deploy
  ⏳ Wait: 1-3 minutes

Step 7: Test
  ✅ Visit: https://your-app.vercel.app
```

---

## 🆘 Getting Help

### Railway Help

- **Documentation:** https://docs.railway.app/
- **Community:** https://discord.gg/railway
- **Status:** https://status.railway.app/

### Vercel Help

- **Documentation:** https://vercel.com/docs
- **Community:** https://github.com/vercel/vercel/discussions
- **Status:** https://www.vercel-status.com/

### This Project

- **GitHub Issues:** Open an issue in your repository
- **Documentation:** Check other `.md` files in this project
- **Logs:** Always check deployment logs first!

---

## 🎓 What You Learned

Congratulations! You now know how to:

- ✅ Deploy a Python backend to Railway
- ✅ Deploy a React frontend to Vercel
- ✅ Configure environment variables
- ✅ Connect frontend to backend across different services
- ✅ Use GitHub Gist for data storage
- ✅ Monitor and troubleshoot deployments
- ✅ Update deployments (auto-deploy from GitHub)

---

## 🚀 Next Steps

Now that your app is deployed:

1. **Share it!** Send the Vercel URL to users
2. **Monitor usage:** Check Railway/Vercel dashboards
3. **Check Gist:** See results accumulating
4. **Improve it:** Add features, push to GitHub, auto-deploys!
5. **Custom domain:** Make it professional (optional)

---

## 📌 Quick Reference

### Your URLs

```
Frontend:  https://your-app.vercel.app
Backend:   https://your-app.railway.app
API Test:  https://your-app.railway.app/api/health
Gist:      https://gist.github.com/yourusername/your_gist_id
```

### Environment Variables Summary

**Railway (Backend):**
- `GITHUB_TOKEN` = Your GitHub personal access token
- `GIST_ID` = Your Gist ID (optional)
- `PORT` = 5000

**Vercel (Frontend):**
- `VITE_API_URL` = Your Railway backend URL

---

**You did it!** 🎉

Your AHP Questionnaire is now live on the internet, accessible to anyone with the URL!

**Happy deploying!** 🚀
