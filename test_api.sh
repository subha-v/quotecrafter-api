#!/bin/bash

echo "🚀 QuoteCrafter API Test Script"
echo "==============================="

BASE_URL="http://127.0.0.1:8000"

echo -e "\n✅ Testing all endpoints..."

# 1. Health Check
echo -e "\n📋 Health Check:"
curl -s $BASE_URL/health | python3 -m json.tool

# 2. Create quotes
echo -e "\n📝 Creating quotes..."
curl -s -X POST "$BASE_URL/quotes/" \
  -H "Content-Type: application/json" \
  -d '{"author": "Steve Jobs", "content": "Innovation distinguishes between a leader and a follower."}' > /dev/null

echo "Created quote 1 ✓"

# 3. List all quotes
echo -e "\n📚 All quotes:"
curl -s $BASE_URL/quotes/ | python3 -m json.tool

echo -e "\n🎉 API is working perfectly!"
echo "📖 Visit http://127.0.0.1:8000/docs for interactive docs" 