"""
Criteria Loading Service
Single Responsibility: Load criteria from various sources
"""

import os
import pandas as pd
from typing import List
from .interfaces import ICriteriaLoader


class CSVCriteriaLoader(ICriteriaLoader):
    """Load criteria from CSV file."""

    DEFAULT_CRITERIA = [
        "Passenger Activity",
        "Service & Modes",
        "Location",
        "Population & Jobs",
        "Bus Terminal"
    ]

    def __init__(self, csv_file: str = "criteria.csv"):
        """Initialize with CSV file path."""
        self.csv_file = csv_file

    def load_criteria(self) -> List[str]:
        """Load criteria from CSV or return defaults."""
        if not os.path.exists(self.csv_file):
            return self.DEFAULT_CRITERIA

        try:
            df = pd.read_csv(self.csv_file)

            # Get first column
            if len(df.columns) == 0:
                return self.DEFAULT_CRITERIA

            column_name = df.columns[0]
            criteria = [
                str(c).strip()
                for c in df[column_name].dropna().tolist()
                if str(c).strip()
            ]

            # Validate minimum criteria
            if len(criteria) < 2:
                return self.DEFAULT_CRITERIA

            return criteria

        except Exception:
            return self.DEFAULT_CRITERIA
