#!/bin/bash
# Test script to diagnose 405 error

API_URL="${1:-http://localhost:5000}"

echo "🧪 Testing AHP Backend API"
echo "API URL: $API_URL"
echo "================================"
echo ""

# Test 1: Health Check
echo "Test 1: Health Check (GET)"
echo "---"
curl -X GET "$API_URL/api/health" \
  -H "Content-Type: application/json" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s
echo ""
echo ""

# Test 2: OPTIONS preflight
echo "Test 2: OPTIONS Preflight (CORS)"
echo "---"
curl -X OPTIONS "$API_URL/api/calculate" \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -w "\nHTTP Status: %{http_code}\n" \
  -v \
  2>&1 | grep -E "(HTTP|Access-Control|< )"
echo ""
echo ""

# Test 3: POST calculate
echo "Test 3: POST Calculate"
echo "---"
curl -X POST "$API_URL/api/calculate" \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:5173" \
  -d '{
    "userName": "Test User",
    "criteria": ["A", "B"],
    "comparisons": [
      {"indexA": 0, "indexB": 1, "value": 0}
    ]
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s
echo ""
echo ""

# Test 4: Check CORS headers
echo "Test 4: Detailed CORS Headers"
echo "---"
curl -X OPTIONS "$API_URL/api/calculate" \
  -H "Origin: http://localhost:5173" \
  -I \
  2>&1 | grep -i "access-control"
echo ""

echo "================================"
echo "✅ Tests complete!"
echo ""
echo "If you see 405 errors, check:"
echo "1. Backend is running and updated"
echo "2. URL is correct"
echo "3. CORS headers are present in response"
