# AHP Weights Calculator

This notebook calculates final aggregated weights from AHP questionnaire participant responses.

## Quick Start

1. **Get your responses CSV**: Export responses from GitHub Gist or collect from your backend
2. **Open the notebook**: `jupyter notebook ahp_weights_calculator.ipynb`
3. **Update the INPUT_CSV path** in the configuration cell
4. **Run all cells**
5. **Get your final weights** from `final_weights.json`

## Input Format

The CSV file should contain responses from all participants with the following columns:

### Required Columns:
- `timestamp`: When the response was submitted
- `user_name`: Participant identifier
- `weight_[criterion_name]`: Individual weight for each criterion (one column per criterion)

### Optional Columns (for filtering):
- `consistency_ratio`: CR value for filtering inconsistent responses
- `consistency_index`: CI value
- `lambda_max`: Maximum eigenvalue
- `is_consistent`: Boolean flag

### Example CSV Format:

```csv
timestamp,user_name,consistency_ratio,consistency_index,lambda_max,is_consistent,weight_Passenger Activity,weight_Service & Modes,weight_Location,weight_Population & Jobs,weight_Bus Terminal
2025-12-25 10:30:00,Alice Smith,0.0523,0.0587,5.2348,True,0.3245,0.2156,0.1823,0.1987,0.0789
2025-12-25 10:45:00,Bob Johnson,0.0872,0.0978,5.3912,True,0.2876,0.2543,0.1654,0.2123,0.0804
...
```

See `example_responses.csv` for a complete example.

## How to Get Your Responses CSV

### Option 1: From GitHub Gist (if using the app's save feature)

The application saves responses to GitHub Gist. You can:

1. Find your Gist URL from the app's responses
2. Download the CSV file from the Gist
3. Combine multiple Gists if you have responses across multiple files

### Option 2: From Backend API

If your backend stores responses, export them with this structure:

```python
import pandas as pd

# Example backend export
responses = []
for response in database.get_all_responses():
    row = {
        'timestamp': response.timestamp,
        'user_name': response.user_name,
        'consistency_ratio': response.cr,
        'consistency_index': response.ci,
        'lambda_max': response.lambda_max,
        'is_consistent': response.is_consistent,
    }
    # Add weights for each criterion
    for criterion, weight in response.weights.items():
        row[f'weight_{criterion}'] = weight

    responses.append(row)

df = pd.DataFrame(responses)
df.to_csv('responses.csv', index=False)
```

## Aggregation Methods

The notebook uses **geometric mean** for aggregation (recommended for AHP):

```
geometric_mean = (w1 × w2 × ... × wn)^(1/n)
```

This preserves the ratio-scale properties of AHP judgments better than arithmetic mean.

## Output Files

The notebook generates:

1. **`final_weights.json`**: Final weights with metadata (use this for scoring)
   ```json
   {
     "metadata": {
       "generated_at": "2025-12-25T12:00:00",
       "total_responses": 10,
       "consistent_responses": 8,
       "consistency_threshold": 0.10,
       "aggregation_method": "geometric_mean"
     },
     "weights": {
       "Passenger Activity": 0.3142,
       "Service & Modes": 0.2234,
       "Location": 0.1856,
       "Population & Jobs": 0.2012,
       "Bus Terminal": 0.0756
     },
     "weights_percentage": {
       "Passenger Activity": 31.42,
       "Service & Modes": 22.34,
       ...
     }
   }
   ```

2. **`final_weights.csv`**: Weights in CSV format
3. **`ahp_weights_visualization.png`**: Visual charts
4. **`weights_calculation_report.txt`**: Summary report

## Using Weights for Scoring

Once you have the final weights, use them to calculate weighted scores:

```python
import json

# Load weights
with open('final_weights.json') as f:
    data = json.load(f)
    weights = data['weights']

# Example: Score a terminal/station
terminal_scores = {
    'Passenger Activity': 8.5,
    'Service & Modes': 7.2,
    'Location': 9.0,
    'Population & Jobs': 6.8,
    'Bus Terminal': 7.5
}

# Calculate weighted final score
final_score = sum(terminal_scores[criterion] * weights[criterion]
                  for criterion in weights)

print(f"Final Score: {final_score:.2f}")
```

## Consistency Filtering

By default, the notebook filters out responses with CR > 0.10 (standard AHP threshold).

- **CR ≤ 0.10**: Acceptable consistency (included)
- **CR > 0.10**: Poor consistency (excluded)

You can adjust `CONSISTENCY_THRESHOLD` in the configuration cell.

## Validation

The notebook performs these validation checks:

- ✓ Sum of weights = 1.0
- ✓ All weights are positive
- ✓ Correct number of criteria
- ✓ No NaN/Inf values

## Customization

### Change aggregation method:
```python
# Use arithmetic mean instead of geometric mean
final_weights = aggregate_weights_arithmetic_mean(consistent_df, weight_columns)
```

### Include all responses (ignore consistency):
```python
CONSISTENCY_THRESHOLD = 1.0  # Accept all responses
```

### Filter by participant:
```python
# Only include specific users
filtered_df = consistent_df[consistent_df['user_name'].isin(['Alice', 'Bob'])]
final_weights = aggregate_weights_geometric_mean(filtered_df, weight_columns)
```

## Requirements

Install required packages:

```bash
pip install pandas numpy scipy matplotlib jupyter
```

Or use the provided requirements file:

```bash
pip install -r requirements.txt
```

## Troubleshooting

### "No such file: responses.csv"
- Update the `INPUT_CSV` path in the configuration cell
- Make sure your CSV file is in the correct location

### "No weight columns found"
- Check that your CSV has columns starting with `weight_`
- Verify the CSV format matches the example

### "Division by zero" errors
- Check for zero or missing values in weight columns
- Ensure all weights are positive numbers

### Weights don't sum to 1.0
- The notebook automatically normalizes weights
- Check the validation section for confirmation

## Support

For issues or questions about:
- The notebook: Check the cell outputs and validation section
- The AHP questionnaire app: See the main project README
- AHP methodology: Refer to Saaty's AHP literature

## References

- Saaty, T.L. (1980). The Analytic Hierarchy Process. McGraw-Hill.
- Saaty, T.L. (2008). Decision making with the analytic hierarchy process.
- Aggregate weights using geometric mean: Recommended by AHP experts for group decision making.
