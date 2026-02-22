#!/bin/bash
# Start the Star Wars GraphDB Web Server

echo "🌟 Starting Star Wars GraphDB Web Server..."
echo ""
echo "📚 Loading configuration..."

# Set environment variables if not already set
if [ -z "$SWAPI_MODEL" ]; then
    export SWAPI_MODEL="gpt-4"
    echo "   Using default model: gpt-4"
else
    echo "   Using model: $SWAPI_MODEL"
fi

if [ -z "$MOONSHOTAI_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "   ⚠️  No API key found. Using pattern matching mode."
else
    echo "   ✓ API key configured"
fi

echo ""
echo "🚀 Starting FastAPI server..."
echo "   URL: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the server
python api.py
