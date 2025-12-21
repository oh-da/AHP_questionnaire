# How to Test Your Backend API (Fix 405 Error)

## 🎯 Goal
Test if your Railway backend has the 405 error fix deployed.

## 📋 Step-by-Step Instructions

### Step 1: Redeploy Your Railway Backend

The 405 fix has been pushed to GitHub, but Railway needs to redeploy:

1. **Go to Railway Dashboard**
   - Visit: https://railway.app
   - Log in to your account

2. **Find Your Backend Service**
   - Click on your project
   - Click on the backend service (the Python API service)

3. **Trigger Redeploy**
   - Go to "Deployments" tab
   - Click the "..." menu on the latest deployment
   - Click "Redeploy"
   - **OR** click "Deploy" button to pull latest code from GitHub

4. **Wait for Deployment** (1-2 minutes)
   - Watch the logs to ensure no errors
   - Wait for status to show "Active" with green checkmark

### Step 2: Get Your Railway Backend URL

1. In Railway, click on your backend service
2. Go to "Settings" tab
3. Scroll to "Public Networking" or "Domains" section
4. Copy the URL - it looks like:
   ```
   https://ahp-backend-production-a1b2c3.up.railway.app
   ```

### Step 3: Run the Test Script

**On your local computer:**

```bash
# Make script executable (first time only)
chmod +x test_api.sh

# Run test with YOUR Railway URL
./test_api.sh https://your-backend-url.railway.app
```

**Replace `https://your-backend-url.railway.app` with your actual Railway URL!**

### Step 4: Check Test Results

**✅ SUCCESS - All tests should show:**
```
Test 1: Health Check (GET)
HTTP Status: 200

Test 2: OPTIONS Preflight (CORS)
HTTP Status: 200
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Methods: GET,POST,OPTIONS

Test 3: POST Calculate
HTTP Status: 200
{"weights": {...}}

Test 4: Detailed CORS Headers
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET,POST,OPTIONS
```

**❌ FAILURE - If you see:**
- `HTTP Status: 405` → Backend not updated, redeploy Railway
- `Connection refused` → Backend not running, check Railway logs
- `404` → Wrong URL, check your Railway backend URL

### Step 5: Test the Actual Frontend

Once the API tests pass:

1. **Go to your Vercel frontend**
   - URL: `https://your-app.vercel.app`

2. **Fill out the questionnaire**
   - Enter your name
   - Add criteria
   - Answer comparisons
   - Submit

3. **Check for errors**
   - Open DevTools (F12)
   - Go to Network tab
   - Look for the `/api/calculate` request
   - Should show "200 OK" (not 405)

## 🐛 Still Getting 405?

If tests fail, check:

1. **Backend URL is correct**
   ```bash
   # Test with curl
   curl https://your-backend-url.railway.app/api/health
   ```

2. **Railway deployed latest code**
   - Check Railway deployment logs
   - Look for "Deployment successful"
   - Check timestamp matches recent redeploy

3. **Frontend has correct backend URL**
   - In Vercel, go to Settings → Environment Variables
   - Check `VITE_API_URL` = your Railway backend URL
   - Redeploy Vercel if you changed it

4. **Check Railway logs**
   - Go to Railway → Your Service → Deployments
   - Click latest deployment → View Logs
   - Look for startup errors

## 📊 What Each Test Does

| Test | Purpose | Expected Result |
|------|---------|-----------------|
| Test 1: GET /api/health | Checks if backend is running | 200 OK |
| Test 2: OPTIONS /api/calculate | Tests CORS preflight (fixes 405) | 200 OK with CORS headers |
| Test 3: POST /api/calculate | Tests actual calculation | 200 OK with results |
| Test 4: CORS headers | Verifies CORS is configured | Shows Access-Control-* headers |

## 🔑 Key Points

- **Vercel** = Frontend only (React UI)
- **Railway** = Backend only (Python API)
- **test_api.sh** = Tests Railway backend
- You CANNOT run test_api.sh "on Vercel" - it tests the backend!

## 💡 Quick Troubleshooting

**"Can't run test_api.sh"**
```bash
# Make it executable
chmod +x test_api.sh

# Run with bash explicitly
bash test_api.sh https://your-backend-url.railway.app
```

**"Connection refused"**
- Backend is not running
- Check Railway service status
- Check if URL is correct

**"404 Not Found"**
- Wrong URL
- Check if you're using Railway backend URL (not Vercel)

**"405 Method Not Allowed"**
- Backend not updated with latest code
- Redeploy Railway with latest GitHub code
- Make sure Railway pulled from branch: `claude/refactor-solid-principles-xfOFm`

---

**Questions?** Check [TROUBLESHOOTING_405.md](TROUBLESHOOTING_405.md) for detailed debugging steps.
