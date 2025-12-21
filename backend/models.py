"""
Domain Models
Single Responsibility: Pure data structures
"""

from dataclasses import dataclass
from typing import Dict, List, Any
from datetime import datetime


@dataclass
class Comparison:
    """Represents a single pairwise comparison."""
    index_a: int
    index_b: int
    value: float


@dataclass
class AHPResults:
    """Contains AHP calculation results."""
    weights: Dict[str, float]
    lambda_max: float
    ci: float  # Consistency Index
    cr: float  # Consistency Ratio
    is_consistent: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'weights': self.weights,
            'lambdaMax': self.lambda_max,
            'ci': self.ci,
            'cr': self.cr,
            'isConsistent': self.is_consistent
        }


@dataclass
class QuestionnaireResponse:
    """Represents a complete questionnaire response."""
    user_name: str
    criteria: List[str]
    comparisons: List[Comparison]
    results: AHPResults
    timestamp: datetime

    def to_csv_row(self) -> Dict[str, Any]:
        """Convert to CSV row format."""
        row = {
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'user_name': self.user_name,
            'consistency_ratio': self.results.cr,
            'consistency_index': self.results.ci,
            'lambda_max': self.results.lambda_max,
            'is_consistent': self.results.is_consistent
        }

        # Add weights
        for criterion in self.criteria:
            row[f'weight_{criterion}'] = self.results.weights.get(criterion, 0.0)

        return row
