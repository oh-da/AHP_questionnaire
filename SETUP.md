# Google Sheets Integration Setup Guide

This guide explains how to set up permanent data storage using Google Sheets for your Streamlit Cloud app.

## Why Google Sheets?

- ✅ **Permanent storage** - Data persists forever, not lost on app restart
- ✅ **Free** - No database costs
- ✅ **Easy to view** - View/analyze results directly in Google Sheets
- ✅ **Automatic** - Users don't need to download anything
- ✅ **Real-time** - Results appear immediately in the spreadsheet

## Setup Steps

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing one)
3. Note your project name

### 2. Enable Google Sheets API

1. In Google Cloud Console, go to **APIs & Services** > **Library**
2. Search for "Google Sheets API"
3. Click **Enable**
4. Also search for "Google Drive API" and enable it

### 3. Create Service Account

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **Service Account**
3. Fill in details:
   - Service account name: `ahp-questionnaire`
   - Description: `Service account for AHP questionnaire data storage`
4. Click **Create and Continue**
5. Skip optional steps, click **Done**

### 4. Create Service Account Key

1. Click on the service account you just created
2. Go to **Keys** tab
3. Click **Add Key** > **Create new key**
4. Choose **JSON** format
5. Click **Create** - a JSON file will download
6. **Keep this file secure!** It contains credentials

### 5. Add Credentials to Streamlit Cloud

1. Go to your Streamlit Cloud dashboard
2. Click on your app
3. Click **Settings** (⚙️)
4. Go to **Secrets**
5. Add this configuration (paste the entire JSON content from step 4):

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"

# Optional: Your email to auto-share the spreadsheet
admin_email = "your-email@gmail.com"
```

6. Click **Save**

### 6. Test the Integration

1. Redeploy your Streamlit app (or wait for auto-deploy)
2. Complete a questionnaire
3. Check the logs - you should see: `✓ Using Google Sheets for permanent storage`
4. A new Google Sheet named "AHP Questionnaire Results" will be created in your service account's Google Drive
5. If you added `admin_email`, the sheet will be automatically shared with you

## Viewing Your Results

### Option 1: Find the Sheet via Service Account

1. Go to [Google Drive](https://drive.google.com/)
2. Look for "AHP Questionnaire Results" (if you set admin_email, it will be shared with you)

### Option 2: Find via Google Sheets API

The sheet is owned by the service account. To access it:
- The app automatically shares it with your email (if admin_email is set)
- Otherwise, note the spreadsheet ID from the logs and manually share it

## Troubleshooting

### "Google Sheets credentials not found in secrets"
- Make sure you added the credentials to Streamlit Cloud Secrets
- Check the format matches the example above
- Redeploy the app

### "Permission denied" or "Sharing failed"
- Make sure Google Drive API is enabled
- Check that admin_email is correct in secrets
- Manually share the spreadsheet with your email

### Results not appearing
- Check app logs for errors
- Verify both Google Sheets API and Google Drive API are enabled
- Ensure service account has proper permissions

## Security Notes

🔒 **Important:**
- Never commit the service account JSON file to Git
- Keep credentials in Streamlit Cloud Secrets only
- The .gitignore file excludes credential files
- Service account has limited permissions (only Sheets/Drive access)

## Local Development

For local testing, create a file `.streamlit/secrets.toml` with the same content. This file is already in .gitignore.

```bash
mkdir -p .streamlit
# Add credentials to .streamlit/secrets.toml
# (same format as above)
```

## Data Format

The Google Sheet will contain:
- **timestamp**: When the questionnaire was completed
- **consistency_ratio, consistency_index, lambda_max**: AHP metrics
- **is_consistent**: Whether answers are consistent
- **weight_[Criterion Name]**: Final weight for each criterion
- **answer_q_N**: User's answer for each question

Each row = one completed questionnaire
