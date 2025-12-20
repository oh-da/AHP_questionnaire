"""
Flask API Server for AHP Questionnaire
Serves the React frontend and provides AHP calculation endpoints
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import numpy as np
from datetime import datetime
import json
import os
import requests
import pandas as pd

app = Flask(__name__, static_folder='frontend/dist')
CORS(app)

# GitHub Gist configuration (from environment variables)
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GIST_ID = os.environ.get('GIST_ID')
GIST_FILENAME = 'ahp_results.csv'

# AHP Calculator (from your existing app.py)
class AHPCalculator:
    def __init__(self):
        self.ri_values = {
            1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
            5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
            9: 1.45, 10: 1.49
        }

    def convert_scale_to_ratio(self, scale_value):
        if scale_value > 0:
            return 1.0 / (scale_value + 1)
        elif scale_value == 0:
            return 1.0
        else:
            return abs(scale_value) + 1

    def calculate_weights(self, criteria, comparisons):
        n = len(criteria)

        # Build matrix
        matrix = np.ones((n, n))
        for comparison in comparisons:
            i, j = comparison['indexA'], comparison['indexB']
            ratio = self.convert_scale_to_ratio(comparison['value'])
            matrix[i, j] = ratio
            matrix[j, i] = 1.0 / ratio

        # Calculate weights using geometric mean
        geometric_means = np.power(np.prod(matrix, axis=1), 1.0 / n)
        weights = geometric_means / geometric_means.sum()

        # Consistency metrics
        weighted_sum = matrix @ weights
        lambda_max = np.mean(weighted_sum / weights)
        ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
        ri = self.ri_values.get(n, 1.12)
        cr = ci / ri if ri > 0 else 0.0

        return {
            'weights': {criteria[i]: float(weights[i]) for i in range(n)},
            'lambdaMax': float(lambda_max),
            'ci': float(ci),
            'cr': float(cr),
            'isConsistent': cr <= 0.1
        }

calculator = AHPCalculator()

# API Routes
@app.route('/api/calculate', methods=['POST'])
def calculate_ahp():
    """Calculate AHP weights from comparisons"""
    try:
        data = request.json
        criteria = data['criteria']
        comparisons = data['comparisons']

        results = calculator.calculate_weights(criteria, comparisons)

        # Save to file (optional)
        save_results(data.get('userName', 'Anonymous'), criteria, comparisons, results)

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/results', methods=['GET'])
def get_results():
    """Get all saved results"""
    try:
        if os.path.exists('results.json'):
            with open('results.json', 'r') as f:
                results = json.load(f)
            return jsonify(results)
        return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve React frontend"""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

def save_to_github_gist(user_name, criteria, results):
    """Save results to GitHub Gist (CSV format)"""
    if not GITHUB_TOKEN:
        print("⚠️  GITHUB_TOKEN not set - skipping Gist save")
        return False

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Build row data
        row_data = {
            'timestamp': timestamp,
            'user_name': user_name,
            'consistency_ratio': results['cr'],
            'consistency_index': results['ci'],
            'lambda_max': results['lambdaMax'],
            'is_consistent': results['isConsistent']
        }

        # Add weights for each criterion
        for criterion, weight in results['weights'].items():
            row_data[f'weight_{criterion}'] = weight

        # Convert to DataFrame
        df_new = pd.DataFrame([row_data])

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Get existing gist content if GIST_ID is set
        csv_content = df_new.to_csv(index=False)
        gist_id = GIST_ID

        if gist_id:
            # Update existing gist - append to CSV
            response = requests.get(
                f"https://api.github.com/gists/{gist_id}",
                headers=headers
            )

            if response.status_code == 200:
                gist_data = response.json()
                existing_content = gist_data["files"][GIST_FILENAME]["content"]

                # Append new row to existing CSV
                df_existing = pd.read_csv(pd.io.common.StringIO(existing_content))
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                csv_content = df_combined.to_csv(index=False)
            else:
                # Gist not found, create new
                gist_id = None

        # Create or update gist
        gist_data = {
            "description": "AHP Questionnaire Results",
            "public": False,
            "files": {
                GIST_FILENAME: {
                    "content": csv_content
                }
            }
        }

        if gist_id:
            # Update existing gist
            response = requests.patch(
                f"https://api.github.com/gists/{gist_id}",
                headers=headers,
                json=gist_data
            )
        else:
            # Create new gist
            response = requests.post(
                "https://api.github.com/gists",
                headers=headers,
                json=gist_data
            )

        if response.status_code in [200, 201]:
            response_data = response.json()
            gist_url = response_data["html_url"]
            print(f"✅ Saved to GitHub Gist: {gist_url}")
            return True
        else:
            print(f"❌ Error saving to Gist: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error saving to GitHub Gist: {e}")
        return False

def save_results(user_name, criteria, comparisons, results):
    """Save results to both local JSON and GitHub Gist"""
    # Save to GitHub Gist (primary storage)
    gist_saved = save_to_github_gist(user_name, criteria, results)

    # Also save to local JSON as backup
    try:
        # Load existing results
        if os.path.exists('results.json'):
            with open('results.json', 'r') as f:
                all_results = json.load(f)
        else:
            all_results = []

        # Add new result
        all_results.append({
            'timestamp': datetime.now().isoformat(),
            'userName': user_name,
            'criteria': criteria,
            'weights': results['weights'],
            'consistency': {
                'cr': results['cr'],
                'ci': results['ci'],
                'lambdaMax': results['lambdaMax'],
                'isConsistent': results['isConsistent']
            }
        })

        # Save
        with open('results.json', 'w') as f:
            json.dump(all_results, f, indent=2)

        if gist_saved:
            print("✅ Results saved to both GitHub Gist and local JSON")
        else:
            print("⚠️  Results saved to local JSON only (GitHub Gist failed)")

    except Exception as e:
        print(f"Error saving to local JSON: {e}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
