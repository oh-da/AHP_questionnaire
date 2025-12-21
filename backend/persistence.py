"""
Persistence Services
Single Responsibility: Data storage and retrieval
"""

import os
import pandas as pd
import requests
from typing import List, Dict, Optional
from io import StringIO
from .interfaces import IPersistenceService
from .models import QuestionnaireResponse


class GitHubGistPersistence(IPersistenceService):
    """
    GitHub Gist persistence implementation.
    Liskov Substitution: Can be substituted with any IPersistenceService.
    """

    def __init__(
        self,
        github_token: Optional[str] = None,
        gist_id: Optional[str] = None,
        filename: str = "ahp_results.csv"
    ):
        """Initialize GitHub Gist persistence."""
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.gist_id = self._normalize_gist_id(gist_id or os.getenv("GIST_ID"))
        self.filename = filename
        self.api_url = "https://api.github.com/gists"

    @staticmethod
    def _normalize_gist_id(raw_gist_id: Optional[str]) -> Optional[str]:
        """Normalize gist ID from URL or raw ID."""
        if not raw_gist_id:
            return None

        cleaned = raw_gist_id.strip()
        if not cleaned:
            return None

        # Extract ID from URL if needed
        if "/" in cleaned:
            cleaned = cleaned.rstrip("/").split("/")[-1]

        return cleaned

    def is_configured(self) -> bool:
        """Check if GitHub token is configured."""
        return self.github_token is not None

    def save_response(self, response: QuestionnaireResponse) -> Dict[str, any]:
        """Save response to GitHub Gist."""
        if not self.is_configured():
            return {
                'saved': False,
                'url': None,
                'message': 'GitHub token not configured'
            }

        try:
            # Convert response to CSV row
            row_data = response.to_csv_row()
            df_new = pd.DataFrame([row_data])

            # Get existing content if gist exists
            csv_content = df_new.to_csv(index=False)

            if self.gist_id:
                csv_content = self._append_to_existing_gist(df_new)

            # Create or update gist
            return self._save_to_gist(csv_content)

        except Exception as e:
            return {
                'saved': False,
                'url': None,
                'message': f'Error saving to gist: {str(e)}'
            }

    def load_responses(self) -> List[Dict]:
        """Load all responses from GitHub Gist."""
        if not self.is_configured() or not self.gist_id:
            return []

        try:
            headers = self._get_headers()
            response = requests.get(
                f"{self.api_url}/{self.gist_id}",
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:
                return []

            gist_data = response.json()
            if self.filename not in gist_data.get("files", {}):
                return []

            csv_content = gist_data["files"][self.filename].get("content", "")
            if not csv_content:
                return []

            df = pd.read_csv(StringIO(csv_content))
            return df.to_dict(orient="records")

        except Exception:
            return []

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for GitHub API."""
        return {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def _append_to_existing_gist(self, df_new: pd.DataFrame) -> str:
        """Append new data to existing gist content."""
        try:
            headers = self._get_headers()
            response = requests.get(
                f"{self.api_url}/{self.gist_id}",
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                gist_data = response.json()
                existing_file = gist_data.get("files", {}).get(self.filename)

                if existing_file and existing_file.get("content"):
                    df_existing = pd.read_csv(StringIO(existing_file["content"]))
                    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                    return df_combined.to_csv(index=False)
        except Exception:
            pass

        return df_new.to_csv(index=False)

    def _save_to_gist(self, csv_content: str) -> Dict[str, any]:
        """Create or update GitHub Gist."""
        headers = self._get_headers()
        payload = {
            "description": "AHP Questionnaire Results",
            "files": {self.filename: {"content": csv_content}}
        }

        if self.gist_id:
            # Update existing gist
            response = requests.patch(
                f"{self.api_url}/{self.gist_id}",
                headers=headers,
                json=payload,
                timeout=30
            )
        else:
            # Create new gist
            payload["public"] = False
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

        if response.status_code in (200, 201):
            json_body = response.json()
            self.gist_id = json_body.get("id", self.gist_id)
            return {
                'saved': True,
                'url': json_body.get("html_url"),
                'gist_id': json_body.get("id"),
                'message': 'Saved to GitHub Gist successfully'
            }

        return {
            'saved': False,
            'url': None,
            'message': f'GitHub API error: {response.status_code}'
        }


class InMemoryPersistence(IPersistenceService):
    """
    In-memory persistence for testing/fallback.
    Liskov Substitution: Can replace GitHubGistPersistence.
    """

    def __init__(self):
        """Initialize in-memory storage."""
        self.responses: List[Dict] = []

    def is_configured(self) -> bool:
        """Always configured."""
        return True

    def save_response(self, response: QuestionnaireResponse) -> Dict[str, any]:
        """Save response to memory."""
        self.responses.append(response.to_csv_row())
        return {
            'saved': True,
            'url': None,
            'message': 'Saved to memory (testing mode)'
        }

    def load_responses(self) -> List[Dict]:
        """Load all responses from memory."""
        return self.responses
