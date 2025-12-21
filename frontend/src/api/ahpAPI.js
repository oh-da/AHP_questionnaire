// API configuration
const apiUrlFromEnv = import.meta.env.VITE_API_URL?.trim();
const API_URL =
  apiUrlFromEnv && apiUrlFromEnv.length > 0
    ? apiUrlFromEnv.replace(/\/$/, '')
    : (typeof window !== 'undefined' && window.location?.origin) || 'http://localhost:5000';

/**
 * Call Flask API to calculate AHP weights and save to GitHub Gist
 */
export async function calculateAHPWithAPI(userName, criteria, answers, comparisons) {
  // Format comparisons for API
  const formattedComparisons = comparisons.map((comp, index) => ({
    indexA: comp.indexA,
    indexB: comp.indexB,
    value: answers[index] || 0
  }));

  let response;

  try {
    response = await fetch(`${API_URL}/api/calculate`, {
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
  } catch (error) {
    throw new Error(`Unable to reach API at ${API_URL}: ${error.message}`);
  }

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`API error ${response.status}: ${message}`);
  }

  const results = await response.json();
  return results;
}

/**
 * Fetch criteria from API
 */
export async function fetchCriteria() {
  let response;

  try {
    response = await fetch(`${API_URL}/api/criteria`);
  } catch (error) {
    throw new Error(`Unable to reach API at ${API_URL}: ${error.message}`);
  }
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  const data = await response.json();
  return data.criteria || [];
}

/**
 * Fetch all saved results from API
 */
export async function fetchResults() {
  let response;

  try {
    response = await fetch(`${API_URL}/api/results`);
  } catch (error) {
    throw new Error(`Unable to reach API at ${API_URL}: ${error.message}`);
  }
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return await response.json();
}
