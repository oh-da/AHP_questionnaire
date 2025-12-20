# GitHub Gist Setup for AHP Questionnaire

This guide shows you how to set up automatic result saving to GitHub Gist (free, permanent cloud storage).

## Why GitHub Gist?

- ✅ **Free** - Unlimited private gists
- ✅ **Permanent** - Your data persists forever
- ✅ **Accessible** - View results anytime at gist.github.com
- ✅ **Versioned** - Every save creates a version (full history)
- ✅ **CSV Format** - Easy to download and analyze in Excel

## 🔑 Step 1: Create a GitHub Personal Access Token

1. Go to [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: `AHP Questionnaire`
4. Select scopes:
   - ✅ **gist** (Create and modify gists)
5. Click "Generate token"
6. **⚠️ IMPORTANT:** Copy the token NOW (you won't see it again!)

Example token: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## 📝 Step 2: Set Environment Variables

### Option A: Export in Terminal

```bash
export GITHUB_TOKEN=ghp_your_token_here
python api_server.py
```

### Option B: Vercel/Production Deployment

1. Go to your Vercel project settings
2. Navigate to "Environment Variables"
3. Add:
   - Name: `GITHUB_TOKEN`
   - Value: `ghp_your_token_here`
4. Redeploy

---

## 🚀 Step 3: Run the Server

```bash
# Make sure environment variable is set
python api_server.py
```

You should see:
```
✅ Saved to GitHub Gist: https://gist.github.com/xxxxx
```

---

## 🎯 Step 4: Complete a Questionnaire

1. Go to your app (localhost:5000 or your Vercel URL)
2. Complete a questionnaire
3. Check the server logs for:
   ```
   ✅ Saved to GitHub Gist: https://gist.github.com/username/xxxxxxxxx
   ```
4. Visit the Gist URL to see your results!

---

## 📊 Step 5: View Your Results

1. Go to [gist.github.com](https://gist.github.com)
2. Click on "Secret gists" (your results are private)
3. Find `ahp_results.csv`
4. Download or view online

Each submission appends a new row to the CSV!

---

## 🔒 Security Notes

- ✅ Gists are **private** by default (only you can see them)
- ⚠️ Never commit your token to git
- ⚠️ Use environment variables in production

---

## 📈 CSV Format

```csv
timestamp,user_name,consistency_ratio,consistency_index,lambda_max,is_consistent,weight_Criterion1,weight_Criterion2,...
2024-01-20 14:30:00,Ohad Dahan,0.0234,0.0123,5.045,True,0.3421,0.2156,...
```

Perfect for Excel, Google Sheets, or Python analysis!

---

## 🎉 You're Done!

Now every questionnaire completion automatically saves to your GitHub Gist!

View all results anytime at: **https://gist.github.com** → Secret gists → `ahp_results.csv`
