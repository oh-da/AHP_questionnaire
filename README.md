# AHP Questionnaire - Hub Prioritization

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Features

- Interactive pairwise comparison questionnaire
- AHP weight calculation with consistency checking
- Visual results with bar charts and tables
- Export to CSV or JSON
- **Versatile criteria loading**: Upload your own criteria via CSV or Excel
- Automatic questionnaire generation for any number of criteria
- SOLID design principles throughout

## Custom Criteria

Upload your own criteria using a CSV file with this format:

```csv
Criterion
Passenger Activity
Service & Modes
Location
Population & Jobs
Bus Terminal
```

See `criteria_example.csv` for a template.
