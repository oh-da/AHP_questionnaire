"""
Application Services
Single Responsibility: Business logic orchestration
"""

from typing import List, Dict, Any
from datetime import datetime
from .interfaces import IAHPCalculator, IPersistenceService, ICriteriaLoader
from .models import Comparison, QuestionnaireResponse


class AHPQuestionnaireService:
    """
    Main business logic service.
    Dependency Inversion: Depends on interfaces, not concrete implementations.
    """

    def __init__(
        self,
        calculator: IAHPCalculator,
        persistence: IPersistenceService,
        criteria_loader: ICriteriaLoader
    ):
        """Initialize service with dependencies."""
        self.calculator = calculator
        self.persistence = persistence
        self.criteria_loader = criteria_loader

    def get_criteria(self) -> List[str]:
        """Get questionnaire criteria."""
        return self.criteria_loader.load_criteria()

    def process_questionnaire(
        self,
        user_name: str,
        criteria: List[str],
        comparisons: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Process complete questionnaire submission.
        Returns results with save status.
        """
        # Validate input
        if not criteria or len(criteria) < 2:
            raise ValueError("At least 2 criteria required")

        if not comparisons:
            raise ValueError("Comparisons required")

        # Convert to domain models
        comparison_objects = [
            Comparison(
                index_a=comp.get("indexA", 0),
                index_b=comp.get("indexB", 0),
                value=comp.get("value", 0.0)
            )
            for comp in comparisons
        ]

        # Calculate AHP results
        results = self.calculator.calculate_weights(criteria, comparison_objects)

        # Create response object
        response = QuestionnaireResponse(
            user_name=user_name,
            criteria=criteria,
            comparisons=comparison_objects,
            results=results,
            timestamp=datetime.utcnow()
        )

        # Save to persistence
        save_result = self.persistence.save_response(response)

        # Build response
        return {
            **results.to_dict(),
            'userName': user_name,
            'criteria': criteria,
            'savedToGist': save_result.get('saved', False),
            'gistUrl': save_result.get('url'),
            'gistId': save_result.get('gist_id'),
            'message': save_result.get('message')
        }

    def get_all_responses(self) -> List[Dict]:
        """Get all saved responses."""
        return self.persistence.load_responses()

    def get_health_status(self) -> Dict[str, Any]:
        """Get service health status."""
        criteria = self.get_criteria()
        return {
            'status': 'ok',
            'criteriaCount': len(criteria),
            'gistConfigured': self.persistence.is_configured()
        }
