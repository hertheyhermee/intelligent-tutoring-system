#!/usr/bin/env python
"""Quick launch script for the Geometry Tutor web interface."""

from src.intelligent_tutoring_system.web.app import run_server

if __name__ == '__main__':
    print("=" * 60)
    print("📐 Geometry Tutor - Intelligent Tutoring System")
    print("=" * 60)
    print("\n🚀 Starting web server...")
    print("📖 Open your browser and go to: http://127.0.0.1:5000")
    print("🛑 Press Ctrl+C to stop the server\n")
    print("=" * 60)
    
    try:
        run_server(debug=True)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
