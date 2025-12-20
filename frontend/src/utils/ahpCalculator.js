/**
 * AHP Calculator
 * Implements the Analytic Hierarchy Process calculation
 */

// Random Index values for different matrix sizes
const RI_VALUES = {
  1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
  5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
  9: 1.45, 10: 1.49
};

/**
 * Convert scale value (-8 to 8) to AHP ratio
 * @param {number} scaleValue - Slider value from -8 to 8
 * @returns {number} - AHP ratio
 */
function convertScaleToRatio(scaleValue) {
  if (scaleValue > 0) {
    return 1.0 / (scaleValue + 1);  // B more important (right side)
  } else if (scaleValue === 0) {
    return 1.0;  // Equal importance
  } else {
    return Math.abs(scaleValue) + 1;  // A more important (left side)
  }
}

/**
 * Build pairwise comparison matrix
 * @param {number} nCriteria - Number of criteria
 * @param {Object} comparisons - Comparison data with indices and values
 * @returns {Array<Array<number>>} - Pairwise matrix
 */
function buildPairwiseMatrix(nCriteria, comparisons) {
  // Initialize matrix with 1s on diagonal
  const matrix = Array(nCriteria).fill(0).map(() =>
    Array(nCriteria).fill(0).map((_, j, arr) => j === arr.indexOf(1) ? 1 : 0)
  );

  // Fill matrix with 1s on diagonal
  for (let i = 0; i < nCriteria; i++) {
    matrix[i][i] = 1;
  }

  // Fill upper triangle and reciprocals in lower triangle
  comparisons.forEach(({ indexA, indexB, ratio }) => {
    matrix[indexA][indexB] = ratio;
    matrix[indexB][indexA] = 1.0 / ratio;  // Reciprocal
  });

  return matrix;
}

/**
 * Calculate geometric mean of array
 * @param {Array<number>} values
 * @returns {number}
 */
function geometricMean(values) {
  const product = values.reduce((acc, val) => acc * val, 1);
  return Math.pow(product, 1.0 / values.length);
}

/**
 * Matrix multiplication
 * @param {Array<Array<number>>} matrix
 * @param {Array<number>} vector
 * @returns {Array<number>}
 */
function matrixVectorMultiply(matrix, vector) {
  return matrix.map(row =>
    row.reduce((sum, val, i) => sum + val * vector[i], 0)
  );
}

/**
 * Calculate AHP weights and consistency metrics
 * @param {Array<string>} criteria - List of criterion names
 * @param {Object} answers - Answers indexed by question number
 * @param {Array<Object>} comparisonList - List of comparisons with indexA, indexB
 * @returns {Object} - Results with weights, lambda_max, ci, cr
 */
export function calculateAHPWeights(criteria, answers, comparisonList) {
  const n = criteria.length;

  // Convert answers to ratios
  const comparisons = comparisonList.map((comp, index) => ({
    indexA: comp.indexA,
    indexB: comp.indexB,
    ratio: convertScaleToRatio(answers[index] || 0)
  }));

  // Build pairwise matrix
  const matrix = buildPairwiseMatrix(n, comparisons);

  // Calculate weights using geometric mean method
  const geometricMeans = matrix.map(row => geometricMean(row));
  const sum = geometricMeans.reduce((acc, val) => acc + val, 0);
  const weights = geometricMeans.map(gm => gm / sum);

  // Calculate lambda_max for consistency
  const weightedSum = matrixVectorMultiply(matrix, weights);
  const lambdaValues = weightedSum.map((val, i) => val / weights[i]);
  const lambdaMax = lambdaValues.reduce((acc, val) => acc + val, 0) / n;

  // Consistency Index (CI)
  const ci = n > 1 ? (lambdaMax - n) / (n - 1) : 0;

  // Consistency Ratio (CR)
  const ri = RI_VALUES[n] || 1.12;
  const cr = ri > 0 ? ci / ri : 0;

  // Build weights object
  const weightsObject = {};
  criteria.forEach((criterion, i) => {
    weightsObject[criterion] = weights[i];
  });

  return {
    weights: weightsObject,
    lambdaMax,
    ci,
    cr,
    isConsistent: cr <= 0.1
  };
}
