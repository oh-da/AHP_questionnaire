# API 405 Error Troubleshooting Guide

If you're getting a 405 error when submitting the questionnaire, follow these steps:

## 🔍 Step 1: Verify Backend is Updated

**Check you have the latest code:**
```bash
git pull origin claude/refactor-solid-principles-xfOFm
```

**Verify the fix is in place:**
```bash
# Check if backend/api.py has the OPTIONS handler
grep -A 5 "if request.method == \"OPTIONS\"" backend/api.py
```

You should see:
```python
if request.method == "OPTIONS":
    response = jsonify({"status": "ok"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response, 200
```

## 🐛 Step 2: Test the API Directly

**Run the test script:**
```bash
./test_api.sh http://your-backend-url.railway.app
```

Or test manually:

**Test OPTIONS (preflight):**
```bash
curl -X OPTIONS http://your-backend-url/api/calculate \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

**Expected response:**
- Status: `200 OK` or `204 No Content`
- Headers should include:
  - `Access-Control-Allow-Origin: *`
  - `Access-Control-Allow-Methods: POST, OPTIONS`

**Test POST:**
```bash
curl -X POST http://your-backend-url/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"userName":"Test","criteria":["A","B"],"comparisons":[{"indexA":0,"indexB":1,"value":0}]}'
```

**Expected response:**
- Status: `200 OK`
- JSON with weights and results

## 🚀 Step 3: Redeploy Backend

### Railway:
1. Go to Railway dashboard
2. Click your service
3. Go to "Deployments"
4. Click "..." on latest deployment
5. Click "Redeploy"
6. Wait for deployment to complete (1-2 minutes)

### Docker:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Manual:
```bash
git pull
pip install -r requirements-backend.txt
# Restart your server
```

## 🌐 Step 4: Clear Browser Cache

Sometimes the browser caches the 405 error:

1. Open DevTools (F12)
2. Go to Network tab
3. Check "Disable cache"
4. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

Or try in incognito/private mode.

## 🔧 Step 5: Check Frontend API URL

**Verify frontend is calling the correct backend:**

1. Open frontend in browser
2. Open DevTools (F12)
3. Go to Console
4. Check what URL is being called when you submit

**In the frontend code, check:**
```bash
# If using Vercel, check environment variable
cat frontend/.env
# or check Vercel dashboard → Settings → Environment Variables
# Should have: VITE_API_URL=https://your-backend.railway.app
```

## 🎯 Step 6: Check Exact Error

**In browser DevTools:**
1. Open Network tab
2. Submit questionnaire
3. Look for failed request (red)
4. Click on it
5. Check:
   - Request URL (is it correct?)
   - Request Method (should be POST)
   - Status Code (405?)
   - Response Headers (are CORS headers present?)

**Common Issues:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| OPTIONS returns 405 | Backend not updated | Redeploy with latest code |
| OPTIONS returns 200 but POST returns 405 | Route mismatch | Check URL is exactly `/api/calculate` |
| No CORS headers | CORS not configured | Verify backend/api.py has CORS setup |
| ERR_CONNECTION_REFUSED | Backend not running | Start backend |
| 404 Not Found | Wrong URL | Check VITE_API_URL |

## 📊 Step 7: Check Logs

**Railway:**
1. Go to your service
2. Click "Deployments"
3. Click latest deployment
4. Click "View Logs"
5. Look for errors or 405 responses

**Docker:**
```bash
docker-compose logs -f backend
```

Look for:
- Startup errors
- Request logs
- 405 responses

## 🔄 Step 8: Full Reset

If nothing works, try a complete redeploy:

### Railway:
1. Delete the service
2. Create new service from GitHub
3. Add environment variables (GITHUB_TOKEN, GIST_ID)
4. Deploy

### Docker:
```bash
docker-compose down -v
docker system prune -a
git pull
docker-compose up -d --build
```

## 💡 Quick Checklist

- [ ] Backend code updated with latest fix
- [ ] Backend redeployed/restarted
- [ ] `test_api.sh` returns 200 for OPTIONS
- [ ] `test_api.sh` returns 200 for POST
- [ ] Frontend VITE_API_URL is correct
- [ ] Browser cache cleared
- [ ] Tried in incognito mode
- [ ] Checked logs for errors
- [ ] CORS headers present in response

## 🆘 Still Not Working?

If you've tried everything above and still getting 405:

1. **Share the full error details:**
   - Exact error message
   - Request URL
   - Request method
   - Response headers
   - Browser console output
   - Backend logs

2. **Check these files have the fix:**
   - `backend/api.py` should have OPTIONS handler
   - `backend/api.py` should have after_request CORS headers

3. **Test with curl:**
   ```bash
   # If this works but browser doesn't, it's a CORS issue
   curl -X POST http://your-backend/api/calculate \
     -H "Content-Type: application/json" \
     -d '{"userName":"Test","criteria":["A","B"],"comparisons":[{"indexA":0,"indexB":1,"value":0}]}'
   ```

---

**Most common fix:** Redeploy the backend with the latest code! 🚀
