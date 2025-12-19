# AHP Questionnaire - Hub Prioritization

## How to Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository and branch
5. Set main file path: `app.py`
6. Deploy!

The app will automatically read criteria from `criteria.csv` and save results to `results.csv`.

## Features

- 📊 Interactive pairwise comparison questionnaire
- 🧮 AHP weight calculation with consistency checking
- 📈 Visual results with bar charts and tables
- 💾 **Automatic result saving** - each completion appended to `results.csv`
- 📥 Export individual results to CSV or JSON
- ⚙️ **Criteria configuration via CSV file** - edit `criteria.csv` to customize
- 🔄 Automatic questionnaire generation for any number of criteria
- 🏗️ SOLID design principles throughout
- ☁️ **Ready for Streamlit Cloud deployment**

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
