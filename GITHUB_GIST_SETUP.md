# GitHub Gist Setup (Simple & Free!)

## Why GitHub Gist?

- ✅ **100% Free** - No quotas or limits
- ✅ **5-Minute Setup** - Just need a GitHub token
- ✅ **Simple** - No complex APIs or service accounts
- ✅ **Permanent Storage** - Results stored forever
- ✅ **Easy to View** - View your CSV directly on GitHub

## Setup Steps

### 1. Create a GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `AHP Questionnaire`
4. Select scope: **`gist`** (just this one checkbox)
5. Click **"Generate token"**
6. **Copy the token** (save it somewhere - you won't see it again!)

### 2. Add Token to Streamlit Cloud Secrets

1. Go to your Streamlit Cloud app
2. Click **Settings** → **Secrets**
3. Add this:

```toml
github_token = "ghp_YOUR_TOKEN_HERE"
```

4. Click **"Save"**
5. Click **"Reboot app"**

That's it! The app will automatically create a gist on the first questionnaire completion.

## Viewing Your Results

After the first questionnaire is completed:

1. Check the **sidebar** in your app
2. You'll see: **"📊 GitHub Gist"**
3. Click **"View Results"**
4. Opens your GitHub Gist with all results in CSV format!

## Optional: Reuse an Existing Gist

If you want to use a specific gist:

1. Create a gist manually at https://gist.github.com
2. Copy the gist ID from the URL:
   ```
   https://gist.github.com/username/GIST_ID_HERE
   ```
3. Add to Streamlit Secrets:
   ```toml
   github_token = "ghp_YOUR_TOKEN_HERE"
   gist_id = "GIST_ID_HERE"
   ```

## Troubleshooting

### "Secret 'github_token' not found"
- Make sure you added the token to Streamlit Cloud Secrets
- Make sure it's spelled exactly: `github_token`
- Reboot the app after adding secrets

### "401 Unauthorized"
- Your token might be expired or invalid
- Generate a new token with `gist` scope

### "403 Forbidden"
- Make sure you selected the `gist` scope when creating the token

## Security Notes

🔒 **Important:**
- Never share your GitHub token
- Never commit it to your repository
- Keep it only in Streamlit Cloud Secrets
- The token only has access to create/update gists (nothing else)

## What Gets Saved?

Each questionnaire completion adds one row to the CSV with:
- Timestamp
- All answers
- All weights
- Consistency metrics

You can download the CSV from GitHub, open in Excel, or use it for analysis!
