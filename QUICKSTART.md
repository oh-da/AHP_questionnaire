# 🚀 Quick Start Guide

## Running the New React Frontend

You have **two easy options** to run the new React design:

---

## ✅ Option 1: One-Command Setup (Easiest)

This builds the React app and starts the Flask API server automatically:

```bash
chmod +x run.sh
./run.sh
```

Then open: **http://localhost:5000**

---

## ✅ Option 2: Manual Setup (More Control)

### Step 1: Build the React Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### Step 2: Start the Flask API Server

```bash
pip install -r requirements-api.txt
python api_server.py
```

Then open: **http://localhost:5000**

---

## 🔧 Development Mode (For Frontend Development)

If you want to work on the React code with hot-reload:

### Terminal 1: React Dev Server
```bash
cd frontend
npm install
npm run dev
```
Opens at: **http://localhost:3000**

### Terminal 2: Flask API (Optional - for backend testing)
```bash
pip install -r requirements-api.txt
python api_server.py
```
Runs at: **http://localhost:5000**

---

## 📊 Original Streamlit App

To run the original Streamlit version:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at: **http://localhost:8501**

---

## 🎯 What's Different?

| Feature | React Frontend | Streamlit |
|---------|---------------|-----------|
| UI Design | Modern card-based, Hebrew RTL | Classic form-based |
| Comparison | Interactive slider | Slider with labels |
| Progress | Dots + bar | Simple counter |
| Results | Animated bar charts | Static charts |
| Export | JSON download | CSV + JSON |
| Speed | Very fast | Moderate |

---

## 🐛 Troubleshooting

**Port 5000 already in use?**
```bash
# Change port in api_server.py (last line):
app.run(debug=True, port=8000)  # Use any free port
```

**npm install fails?**
```bash
# Make sure you have Node.js 18+
node --version

# Try clearing cache
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Flask import errors?**
```bash
# Make sure you're using the right requirements file
pip install -r requirements-api.txt
```

---

## 📦 Project Structure

```
AHP_questionnaire/
├── frontend/              # React app (NEW!)
│   ├── src/
│   ├── package.json
│   └── README.md
├── api_server.py         # Flask API (NEW!)
├── app.py                # Streamlit app (Original)
├── run.sh                # One-command runner (NEW!)
├── requirements.txt      # Streamlit dependencies
└── requirements-api.txt  # Flask dependencies (NEW!)
```

---

## 🎉 Next Steps

1. **Merge the PR** to integrate the new React frontend
2. **Test the app** locally with `./run.sh`
3. **Customize criteria** by editing the settings in the welcome screen
4. **Deploy** to your preferred hosting (Vercel, Netlify, etc.)

Happy prioritizing! 🎯
