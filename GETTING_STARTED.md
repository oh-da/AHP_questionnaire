# Getting Started - Complete Guide for Beginners 🚀

This guide will help you set up and run the AHP Questionnaire application from scratch, even if you've never done this before.

## 📋 What You'll Need

Before starting, you'll need to install these programs on your computer:

1. **Git** - To download the code
2. **Python 3.8+** - To run the backend server
3. **Node.js 16+** - To run the frontend
4. **A text editor** - Like VS Code (optional but recommended)

---

## 🔧 Step 1: Install Required Software

### Windows

1. **Install Python:**
   - Go to https://www.python.org/downloads/
   - Download Python 3.11 (or latest)
   - **IMPORTANT:** Check "Add Python to PATH" during installation
   - Click "Install Now"

2. **Install Node.js:**
   - Go to https://nodejs.org/
   - Download the LTS version
   - Run the installer (click Next → Next → Install)

3. **Install Git:**
   - Go to https://git-scm.com/download/win
   - Download and install
   - Use default settings

### macOS

1. **Install Homebrew** (if you don't have it):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python, Node.js, and Git:**
   ```bash
   brew install python node git
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip nodejs npm git
```

---

## 📥 Step 2: Download the Application

1. **Open Terminal/Command Prompt:**
   - **Windows:** Press `Win + R`, type `cmd`, press Enter
   - **macOS:** Press `Cmd + Space`, type `terminal`, press Enter
   - **Linux:** Press `Ctrl + Alt + T`

2. **Clone the repository:**
   ```bash
   git clone https://github.com/oh-da/AHP_questionnaire.git
   cd AHP_questionnaire
   ```

   This downloads all the code to your computer and enters the folder.

---

## ⚙️ Step 3: Set Up GitHub Gist (Optional but Recommended)

GitHub Gist provides **free, permanent storage** for your questionnaire results.

### 3.1 Create a GitHub Account

If you don't have one:
1. Go to https://github.com/
2. Click "Sign up"
3. Follow the steps to create an account

### 3.2 Create a Personal Access Token

1. **Log in to GitHub**
2. **Click your profile picture** (top right) → Settings
3. **Scroll down** → Click "Developer settings" (bottom left)
4. **Click "Personal access tokens"** → "Tokens (classic)"
5. **Click "Generate new token"** → "Generate new token (classic)"
6. **Fill in:**
   - Note: `AHP Questionnaire`
   - Expiration: `No expiration` (or choose a date)
   - **Check ONLY:** `gist` (under "Select scopes")
7. **Click "Generate token"** (at the bottom)
8. **IMPORTANT:** Copy the token (starts with `ghp_...`) - you won't see it again!

### 3.3 Create a Gist (Optional)

You can create a new empty Gist, or the app will create one automatically:

1. Go to https://gist.github.com/
2. Click "New gist"
3. Filename: `ahp_results.csv`
4. Add some initial content:
   ```
   timestamp,user_name
   ```
5. Select "Create secret gist"
6. **Copy the Gist ID** from the URL:
   - URL looks like: `https://gist.github.com/yourusername/abc123def456`
   - Gist ID is: `abc123def456`

---

## 🎯 Step 4: Configure the Application

### Option A: Using Environment Variables (Recommended)

**Windows (Command Prompt):**
```cmd
set GITHUB_TOKEN=ghp_your_token_here
set GIST_ID=your_gist_id_here
```

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
$env:GIST_ID="your_gist_id_here"
```

**macOS/Linux:**
```bash
export GITHUB_TOKEN=ghp_your_token_here
export GIST_ID=your_gist_id_here
```

### Option B: Using .env File (Permanent)

Create a file named `.env` in the project folder:

**Windows:**
```cmd
echo GITHUB_TOKEN=ghp_your_token_here > .env
echo GIST_ID=your_gist_id_here >> .env
```

**macOS/Linux:**
```bash
cat > .env << EOF
GITHUB_TOKEN=ghp_your_token_here
GIST_ID=your_gist_id_here
EOF
```

Replace `ghp_your_token_here` and `your_gist_id_here` with your actual values!

---

## 🚀 Step 5: Run the Backend Server

### Quick Method (Recommended)

**macOS/Linux:**
```bash
chmod +x start_backend.sh
./start_backend.sh
```

**Windows:**
```cmd
python -m pip install -r requirements-backend.txt
python -m backend.main
```

### Manual Method

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements-backend.txt
   ```

2. **Start the server:**
   ```bash
   python -m backend.main
   ```

You should see:
```
==================================================
AHP Questionnaire API Server
==================================================

✓ GitHub Gist persistence configured
✓ Server starting on port 5000
✓ Health check: http://localhost:5000/api/health

Press CTRL+C to stop
```

**Keep this terminal window open!** The server needs to keep running.

---

## 🎨 Step 6: Run the Frontend

1. **Open a NEW terminal/command prompt** (keep the backend running!)

2. **Navigate to the frontend folder:**
   ```bash
   cd frontend
   ```

3. **Install dependencies** (first time only):
   ```bash
   npm install
   ```

   This might take 2-5 minutes. ☕

4. **Start the frontend:**
   ```bash
   npm run dev
   ```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## 🎉 Step 7: Use the Application

1. **Open your web browser** (Chrome, Firefox, Safari, etc.)

2. **Go to:** http://localhost:5173/

3. **You should see the AHP Questionnaire!** 🎊

### How to Use:

1. **Enter your name** (optional)
2. **Review the criteria** you'll be comparing
3. **Click "התחל" (Start)**
4. **Answer each comparison** by moving the slider:
   - Move LEFT: Left criterion is more important
   - Stay at 0: Both equally important
   - Move RIGHT: Right criterion is more important
5. **Click through all questions**
6. **View your results!**

Your results are automatically saved to GitHub Gist! 🎯

---

## 🛑 How to Stop the Application

1. **Stop the Frontend:**
   - Go to the terminal running `npm run dev`
   - Press `Ctrl + C`

2. **Stop the Backend:**
   - Go to the terminal running `python -m backend.main`
   - Press `Ctrl + C`

---

## 🔄 How to Start Again Later

You don't need to reinstall everything! Just:

1. **Open Terminal/Command Prompt**

2. **Navigate to the project:**
   ```bash
   cd path/to/AHP_questionnaire
   ```

3. **Set environment variables** (if not using .env file):
   ```bash
   # macOS/Linux
   export GITHUB_TOKEN=ghp_your_token_here
   export GIST_ID=your_gist_id_here

   # Windows
   set GITHUB_TOKEN=ghp_your_token_here
   set GIST_ID=your_gist_id_here
   ```

4. **Start backend** (in one terminal):
   ```bash
   python -m backend.main
   ```

5. **Start frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

6. **Open browser:** http://localhost:5173/

---

## 🐛 Troubleshooting

### "python is not recognized"

**Solution:** Python not in PATH. Try:
- Windows: Use `py` instead of `python`
- Reinstall Python and check "Add to PATH"

### "npm is not recognized"

**Solution:** Node.js not installed or not in PATH.
- Restart terminal after installing Node.js
- Or reinstall Node.js

### Port 5000 already in use

**Solution:** Another program is using port 5000.

**Option 1:** Stop the other program

**Option 2:** Use a different port:
```bash
# Windows
set PORT=3000
python -m backend.main

# macOS/Linux
PORT=3000 python -m backend.main
```

Then update frontend `.env`:
```
VITE_API_URL=http://localhost:3000
```

### Frontend can't connect to backend

**Check:**
1. Backend is running (terminal shows "Server starting...")
2. Backend is on port 5000 (or update `VITE_API_URL`)
3. No firewall blocking localhost connections

### Results not saving to GitHub Gist

**Check:**
1. `GITHUB_TOKEN` is set correctly (starts with `ghp_`)
2. Token has `gist` permission
3. Check backend terminal for error messages

### "ModuleNotFoundError"

**Solution:** Install dependencies:
```bash
pip install -r requirements-backend.txt
```

---

## 📱 Accessing from Other Devices

Want to use the app on your phone or another computer?

1. **Find your computer's IP address:**

   **Windows:**
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (like `192.168.1.100`)

   **macOS/Linux:**
   ```bash
   ifconfig | grep "inet "
   ```

2. **Start backend with host flag:**
   ```bash
   # Edit backend/main.py, change:
   api.run(host="0.0.0.0", port=5000)
   ```

3. **Start frontend with host flag:**
   ```bash
   npm run dev -- --host
   ```

4. **On other device, visit:**
   - Frontend: `http://YOUR_IP:5173`
   - Example: `http://192.168.1.100:5173`

**Note:** Both devices must be on the same WiFi network!

---

## 💡 Tips

- **Keep both terminals open** while using the app
- **Bookmark** http://localhost:5173/ for easy access
- **Check your Gist** at https://gist.github.com/ to see saved results
- **Read the README.md** for more advanced configuration

---

## 📞 Need Help?

- **Check the main README.md** for more details
- **Check REFACTORING_SUMMARY.md** to understand the architecture
- **Open an issue** on GitHub: https://github.com/oh-da/AHP_questionnaire/issues

---

## ✅ Quick Checklist

- [ ] Python installed and working (`python --version`)
- [ ] Node.js installed and working (`node --version`)
- [ ] Git installed and working (`git --version`)
- [ ] Repository cloned (`cd AHP_questionnaire`)
- [ ] GitHub token created (optional)
- [ ] Environment variables set (optional)
- [ ] Backend dependencies installed (`pip install -r requirements-backend.txt`)
- [ ] Frontend dependencies installed (`cd frontend && npm install`)
- [ ] Backend running (`python -m backend.main`)
- [ ] Frontend running (`cd frontend && npm run dev`)
- [ ] Browser opened at http://localhost:5173/
- [ ] Application works! 🎉

---

**Congratulations! You're all set up!** 🎊

Happy prioritizing with AHP! 📊
