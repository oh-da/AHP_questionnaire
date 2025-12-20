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

app = Flask(__name__, static_folder='frontend/dist')
CORS(app)

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

def save_results(user_name, criteria, comparisons, results):
    """Save results to JSON file"""
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
    except Exception as e:
        print(f"Error saving results: {e}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
