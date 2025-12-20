# AHP Questionnaire - Hub Prioritization

A modern questionnaire application using the Analytic Hierarchy Process (AHP) for multi-criteria decision making.

## 🆕 NEW: Modern React Frontend

We now have a beautiful React frontend with Hebrew RTL support! See [frontend/README.md](frontend/README.md) for details.

## Quick Start

### Option 1: React Frontend with Flask API (Recommended - New Design!)

```bash
# Make script executable
chmod +x run.sh

# Run everything (builds React + starts Flask server)
./run.sh
```

Then visit: **http://localhost:5000**

### Option 2: Original Streamlit App

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

Then visit: **http://localhost:8501**

## Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository and branch
5. Set main file path: `app.py`
6. Deploy!

The app will automatically read criteria from `criteria.csv` and save results to `results.csv`.

## Features

### React Frontend
- 🎨 Modern, clean UI with Tailwind CSS
- 🇮🇱 Full Hebrew RTL support
- 📱 Responsive design
- 🎯 Interactive slider-based comparisons
- 📊 Real-time weight calculation
- ✅ Consistency checking (CR, CI, Lambda Max)
- 📈 Beautiful bar chart visualizations
- 💾 Download results as JSON

### Streamlit Version (Legacy)
- 📊 Interactive pairwise comparison questionnaire
- 🧮 AHP weight calculation with consistency checking
- 📈 Visual results with bar charts and tables
- 💾 Automatic result saving to `results.csv`
- 📥 Export individual results to CSV or JSON
- ⚙️ Criteria configuration via CSV file
- 🏗️ SOLID design principles throughout

## Customizing Criteria

Edit `criteria.csv` to define your own criteria:

```csv
Criterion
Passenger Activity
Service & Modes
Location
Population & Jobs
Bus Terminal
```

The questionnaire will automatically generate all pairwise comparisons based on the criteria in this file.

## Data Storage

- **criteria.csv**: Define questionnaire criteria (editable)
- **results.csv**: Stores all completed questionnaires with timestamp (auto-generated)
