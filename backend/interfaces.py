"""
Interfaces (Abstract Base Classes)
Dependency Inversion: High-level modules depend on abstractions
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from .models import AHPResults, QuestionnaireResponse, Comparison


class IAHPCalculator(ABC):
    """Interface for AHP calculations."""

    @abstractmethod
    def calculate_weights(
        self,
        criteria: List[str],
        comparisons: List[Comparison]
    ) -> AHPResults:
        """Calculate AHP weights from pairwise comparisons."""
        pass


class IPersistenceService(ABC):
    """Interface for data persistence."""

    @abstractmethod
    def save_response(self, response: QuestionnaireResponse) -> Dict[str, any]:
        """
        Save questionnaire response.
        Returns dict with: {'saved': bool, 'url': Optional[str], 'message': str}
        """
        pass

    @abstractmethod
    def load_responses(self) -> List[Dict]:
        """Load all saved responses."""
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Check if persistence is properly configured."""
        pass


class ICriteriaLoader(ABC):
    """Interface for loading criteria."""

    @abstractmethod
    def load_criteria(self) -> List[str]:
        """Load questionnaire criteria."""
        pass
