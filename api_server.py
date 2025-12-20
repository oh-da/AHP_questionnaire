import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Environment configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GIST_ID = os.getenv("GIST_ID")
GIST_FILENAME = os.getenv("GIST_FILENAME", "ahp_results.csv")
PORT = int(os.getenv("PORT", "5000"))

# Random Index values for AHP consistency calculation
RI_VALUES: Dict[int, float] = {
    1: 0.00,
    2: 0.00,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49,
}

results_cache: List[Dict[str, Any]] = []


def load_criteria() -> List[str]:
    """Load questionnaire criteria from criteria.csv or fall back to defaults."""
    csv_path = "criteria.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        column_name = df.columns[0]
        return [c for c in df[column_name].dropna().tolist() if str(c).strip()]

    return [
        "Passenger Activity",
        "Service & Modes",
        "Location",
        "Population & Jobs",
        "Bus Terminal",
    ]


CRITERIA = load_criteria()


def convert_scale_to_ratio(scale_value: float) -> float:
    """Convert -8..8 slider scale to AHP ratio."""
    if scale_value > 0:
        return 1.0 / (scale_value + 1)
    if scale_value == 0:
        return 1.0
    return abs(scale_value) + 1


def build_pairwise_matrix(n_criteria: int, comparisons: Dict[tuple, float]) -> np.ndarray:
    """Build full pairwise matrix from comparison ratios."""
    matrix = np.ones((n_criteria, n_criteria))
    for (i, j), value in comparisons.items():
        if i < j:
            matrix[i, j] = value
            matrix[j, i] = 1.0 / value
    return matrix


def calculate_ahp(criteria: List[str], comparisons: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate AHP weights and consistency metrics."""
    n = len(criteria)
    ratio_map = {
        (comp["indexA"], comp["indexB"]): convert_scale_to_ratio(comp.get("value", 0))
        for comp in comparisons
    }

    matrix = build_pairwise_matrix(n, ratio_map)
    geometric_means = np.power(np.prod(matrix, axis=1), 1.0 / n)
    weights = geometric_means / geometric_means.sum()

    weighted_sum = matrix @ weights
    lambda_max = float(np.mean(weighted_sum / weights))
    ci = float((lambda_max - n) / (n - 1)) if n > 1 else 0.0
    ri = RI_VALUES.get(n, 1.12)
    cr = float(ci / ri) if ri > 0 else 0.0

    weights_dict = {criteria[i]: float(weights[i]) for i in range(n)}

    return {
        "weights": weights_dict,
        "lambdaMax": lambda_max,
        "ci": ci,
        "cr": cr,
        "isConsistent": cr <= 0.1,
    }


def build_row_data(user_name: str, criteria: List[str], results: Dict[str, Any]) -> Dict[str, Any]:
    """Build a single CSV row with weights and metadata."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    row_data: Dict[str, Any] = {
        "timestamp": timestamp,
        "user_name": user_name,
        "consistency_ratio": results["cr"],
        "consistency_index": results["ci"],
        "lambda_max": results["lambdaMax"],
        "is_consistent": results["isConsistent"],
    }

    for criterion in criteria:
        row_data[f"weight_{criterion}"] = results["weights"].get(criterion)

    return row_data


def save_to_github_gist(row_data: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """Persist results to GitHub Gist in CSV format."""
    global GIST_ID
    if not GITHUB_TOKEN:
        return {"saved": False, "message": "GITHUB_TOKEN not set", "gist_url": None, "gist_id": GIST_ID}

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    gist_id = GIST_ID
    df_new = pd.DataFrame([row_data])
    csv_content = df_new.to_csv(index=False)

    if gist_id:
        response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers, timeout=30)
        if response.status_code == 200:
            gist_data = response.json()
            existing_file = gist_data.get("files", {}).get(GIST_FILENAME)
            if existing_file and existing_file.get("content"):
                try:
                    df_existing = pd.read_csv(pd.io.common.StringIO(existing_file["content"]))
                    combined = pd.concat([df_existing, df_new], ignore_index=True)
                    csv_content = combined.to_csv(index=False)
                except Exception:
                    csv_content = df_new.to_csv(index=False)
        else:
            gist_id = None

    payload = {
        "description": "AHP Questionnaire Results",
        "files": {GIST_FILENAME: {"content": csv_content}},
    }

    if gist_id:
        response = requests.patch(
            f"https://api.github.com/gists/{gist_id}", headers=headers, json=payload, timeout=30
        )
    else:
        payload["public"] = False
        response = requests.post("https://api.github.com/gists", headers=headers, json=payload, timeout=30)

    if response.status_code in (200, 201):
        json_body = response.json()
        GIST_ID = json_body.get("id") or GIST_ID
        return {
            "saved": True,
            "gist_url": json_body.get("html_url"),
            "gist_id": json_body.get("id"),
            "message": "Saved to GitHub Gist",
        }

    return {
        "saved": False,
        "gist_url": None,
        "gist_id": gist_id,
        "message": f"GitHub API error {response.status_code}",
    }


def load_results_from_gist() -> List[Dict[str, Any]]:
    """Fetch existing results from GitHub Gist if configured."""
    if not (GITHUB_TOKEN and GIST_ID):
        return []

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    response = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=headers, timeout=30)
    if response.status_code != 200:
        return []

    gist_data = response.json()
    if GIST_FILENAME not in gist_data.get("files", {}):
        return []

    csv_content = gist_data["files"][GIST_FILENAME].get("content", "")
    if not csv_content:
        return []

    df = pd.read_csv(pd.io.common.StringIO(csv_content))
    return df.to_dict(orient="records")


@app.route("/api/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "criteriaCount": len(CRITERIA),
            "gistConfigured": bool(GITHUB_TOKEN),
            "gistId": GIST_ID,
        }
    )


@app.route("/api/criteria")
def get_criteria():
    return jsonify({"criteria": CRITERIA})


@app.route("/api/results", methods=["GET"])
def list_results():
    if GITHUB_TOKEN and GIST_ID:
        gist_results = load_results_from_gist()
        if gist_results:
            return jsonify(gist_results)
    return jsonify(results_cache)


@app.route("/api/calculate", methods=["POST"])
def calculate_and_save():
    payload = request.get_json(silent=True) or {}
    user_name = payload.get("userName", "")
    criteria = payload.get("criteria") or CRITERIA
    comparisons = payload.get("comparisons", [])

    if not isinstance(criteria, list) or not criteria:
        return jsonify({"error": "criteria must be a non-empty list"}), 400

    if not isinstance(comparisons, list) or not comparisons:
        return jsonify({"error": "comparisons must be a non-empty list"}), 400

    results = calculate_ahp(criteria, comparisons)
    row_data = build_row_data(user_name, criteria, results)

    gist_response = save_to_github_gist(row_data)
    results_cache.append({**row_data, "gist_url": gist_response.get("gist_url")})

    response_body = {
        **results,
        "userName": user_name,
        "criteria": criteria,
        "savedToGist": gist_response.get("saved", False),
        "gistUrl": gist_response.get("gist_url"),
        "gistId": gist_response.get("gist_id"),
        "message": gist_response.get("message"),
    }

    status_code = 200 if gist_response.get("saved", False) or not GITHUB_TOKEN else 500
    return jsonify(response_body), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
