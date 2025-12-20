# 🚀 Deployment Guide

## Deploying the AHP Questionnaire

You have **two versions** of the app with different deployment options:

---

## 📊 Option 1: Streamlit Cloud (Original UI)

### Pros:
- ✅ Free and easy
- ✅ Works with existing `app.py`
- ✅ No build step needed
- ✅ Auto-saves to CSV

### Steps:

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repo: `oh-da/AHP_questionnaire`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Done!** Your app will be at:
   ```
   https://yourapp.streamlit.app
   ```

### Note:
This deploys the **original Streamlit UI**, not the new React design.

---

## 🎨 Option 2: Vercel (New React UI)

### Pros:
- ✅ Modern React design
- ✅ Hebrew RTL support
- ✅ Lightning fast
- ✅ Free SSL

### Steps:

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy Frontend**
   ```bash
   cd frontend
   vercel
   ```

3. **Follow prompts:**
   - Set up and deploy: Yes
   - Which scope: Your account
   - Link to existing project: No
   - Project name: ahp-questionnaire
   - In which directory: ./ (current)
   - Override settings: No

4. **Done!** Your app will be at:
   ```
   https://ahp-questionnaire.vercel.app
   ```

### Auto-Deploy Setup:
After first deploy, connect your GitHub repo in Vercel dashboard for auto-deployments on push.

---

## 🌐 Option 3: Netlify (New React UI)

### Pros:
- ✅ Great for static sites
- ✅ Easy drag-and-drop
- ✅ Free tier generous

### Steps:

1. **Build React App**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Deploy via CLI**
   ```bash
   npm i -g netlify-cli
   netlify deploy --prod --dir=dist
   ```

   **OR via Web UI:**
   - Go to [app.netlify.com](https://app.netlify.com)
   - Drag `frontend/dist` folder
   - Done!

3. **Your app will be at:**
   ```
   https://random-name.netlify.app
   ```

### Configure Custom Domain (Optional):
Go to Site Settings → Domain Management → Add custom domain

---

## 🔧 Option 4: GitHub Pages (New React UI)

### Pros:
- ✅ Completely free
- ✅ Integrated with GitHub
- ✅ Easy to update

### Steps:

1. **Update `frontend/vite.config.js`**
   ```javascript
   export default defineConfig({
     plugins: [react()],
     base: '/AHP_questionnaire/',  // Add this line
     // ... rest of config
   })
   ```

2. **Add deploy script to `frontend/package.json`**
   ```json
   {
     "scripts": {
       "deploy": "vite build && gh-pages -d dist"
     }
   }
   ```

3. **Install and deploy**
   ```bash
   cd frontend
   npm install gh-pages --save-dev
   npm run deploy
   ```

4. **Enable GitHub Pages**
   - Go to repo Settings → Pages
   - Source: Deploy from branch
   - Branch: gh-pages → root
   - Save

5. **Your app will be at:**
   ```
   https://oh-da.github.io/AHP_questionnaire/
   ```

---

## 🔀 Option 5: Both (Hybrid)

Deploy both versions and let users choose:

1. **Streamlit** (Original) → `https://ahp.streamlit.app`
2. **Vercel/Netlify** (React) → `https://ahp.vercel.app`

Add this to your Streamlit app header:

```python
# At top of app.py
st.info("🆕 Try our [new modern interface](https://ahp.vercel.app)!")
```

---

## 📱 Recommendations by Use Case

| Use Case | Best Option | Why |
|----------|------------|-----|
| Quick demo | Streamlit Cloud | Zero config needed |
| Production use | Vercel | Best performance, auto-deploy |
| Long-term free | GitHub Pages | No costs, reliable |
| Testing | Local (./run.sh) | Fastest iteration |

---

## 🐛 Common Issues

### Vercel: Build fails
```bash
# Make sure you're in the frontend directory
cd frontend
vercel
```

### Netlify: Blank page after deploy
Check that build settings are:
- Build command: `npm run build`
- Publish directory: `dist`

### GitHub Pages: 404 errors
Make sure you set the `base` in `vite.config.js` to match your repo name.

---

## 🔐 Environment Variables

If you add backend API later, set environment variables in your deployment platform:

**Vercel:**
```bash
vercel env add VITE_API_URL
```

**Netlify:**
Go to Site Settings → Environment Variables → Add

---

## 📊 Backend API Deployment

If you want to deploy the Flask API (`api_server.py`):

### Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select your repo
4. Set start command: `python api_server.py`
5. Done!

### Render
1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect repo
4. Build: `pip install -r requirements-api.txt`
5. Start: `python api_server.py`

---

## 🎯 Recommended Setup

For best results:

1. **Frontend (React)** → Vercel
2. **Backend (Optional Flask API)** → Railway
3. **Original Streamlit** → Streamlit Cloud (as fallback)

This gives you:
- Fast, modern UI
- API for data persistence
- Original version as backup

---

## 📞 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Netlify Docs**: https://docs.netlify.com
- **Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud

Happy deploying! 🚀
