// API configuration
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Call Flask API to calculate AHP weights and save to GitHub Gist
 */
export async function calculateAHPWithAPI(userName, criteria, answers, comparisons) {
  try {
    // Format comparisons for API
    const formattedComparisons = comparisons.map((comp, index) => ({
      indexA: comp.indexA,
      indexB: comp.indexB,
      value: answers[index] || 0
    }));

    const response = await fetch(`${API_URL}/api/calculate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userName,
        criteria,
        comparisons: formattedComparisons
      })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const results = await response.json();
    return results;
  } catch (error) {
    console.error('Error calling API:', error);
    // Fall back to local calculation
    return null;
  }
}

/**
 * Fetch all saved results from API
 */
export async function fetchResults() {
  try {
    const response = await fetch(`${API_URL}/api/results`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching results:', error);
    return [];
  }
}
