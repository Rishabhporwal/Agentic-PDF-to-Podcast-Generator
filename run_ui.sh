#!/bin/bash
# Launch Streamlit UI for PDF to Podcast Generator

echo "🚀 Starting PDF to Podcast Generator UI..."
echo "📍 Opening in browser: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py --server.port 8501 --server.headless true
