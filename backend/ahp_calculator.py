"""
AHP Calculator Implementation
Single Responsibility: Pure AHP calculation logic
"""

import numpy as np
from typing import List, Dict
from .interfaces import IAHPCalculator
from .models import AHPResults, Comparison


class AHPCalculator(IAHPCalculator):
    """
    Implements AHP weight calculation using geometric mean method.
    Open/Closed: Can be extended without modification.
    """

    # Random Index values for consistency calculation
    RI_VALUES: Dict[int, float] = {
        1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
        5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
        9: 1.45, 10: 1.49
    }

    def calculate_weights(
        self,
        criteria: List[str],
        comparisons: List[Comparison]
    ) -> AHPResults:
        """Calculate AHP weights and consistency metrics."""
        n = len(criteria)

        # Convert comparisons to ratio matrix
        matrix = self._build_pairwise_matrix(n, comparisons)

        # Calculate weights using geometric mean
        weights = self._calculate_geometric_mean_weights(matrix, n)

        # Calculate consistency metrics
        lambda_max = self._calculate_lambda_max(matrix, weights)
        ci = self._calculate_ci(lambda_max, n)
        cr = self._calculate_cr(ci, n)

        # Build weights dictionary
        weights_dict = {criteria[i]: float(weights[i]) for i in range(n)}

        return AHPResults(
            weights=weights_dict,
            lambda_max=float(lambda_max),
            ci=float(ci),
            cr=float(cr),
            is_consistent=cr <= 0.1
        )

    def _convert_scale_to_ratio(self, scale_value: float) -> float:
        """
        Convert -8..8 scale to AHP ratio.
        - Positive: B more important (1/x)
        - Zero: Equal importance (1.0)
        - Negative: A more important (x)
        """
        if scale_value > 0:
            return 1.0 / (scale_value + 1)
        elif scale_value == 0:
            return 1.0
        else:
            return abs(scale_value) + 1

    def _build_pairwise_matrix(
        self,
        n: int,
        comparisons: List[Comparison]
    ) -> np.ndarray:
        """Build full pairwise comparison matrix."""
        matrix = np.ones((n, n))

        for comp in comparisons:
            ratio = self._convert_scale_to_ratio(comp.value)
            i, j = comp.index_a, comp.index_b

            if i < j:
                matrix[i, j] = ratio
                matrix[j, i] = 1.0 / ratio

        return matrix

    def _calculate_geometric_mean_weights(
        self,
        matrix: np.ndarray,
        n: int
    ) -> np.ndarray:
        """Calculate weights using geometric mean method."""
        geometric_means = np.power(np.prod(matrix, axis=1), 1.0 / n)
        weights = geometric_means / geometric_means.sum()
        return weights

    def _calculate_lambda_max(
        self,
        matrix: np.ndarray,
        weights: np.ndarray
    ) -> float:
        """Calculate lambda max for consistency check."""
        weighted_sum = matrix @ weights
        return float(np.mean(weighted_sum / weights))

    def _calculate_ci(self, lambda_max: float, n: int) -> float:
        """Calculate Consistency Index."""
        if n <= 1:
            return 0.0
        return (lambda_max - n) / (n - 1)

    def _calculate_cr(self, ci: float, n: int) -> float:
        """Calculate Consistency Ratio."""
        ri = self.RI_VALUES.get(n, 1.12)
        if ri == 0:
            return 0.0
        return ci / ri
