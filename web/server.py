#!/usr/bin/env python3
"""
Simple HTTP server for GitFlow AI landing page
"""

import http.server
import socketserver
import webbrowser
import os
import sys

def start_server(port=8000):
    """Start the web server"""
    # Change to web directory
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"🚀 GitFlow AI Landing Page Server")
            print(f"📍 Server running at: http://localhost:{port}")
            print(f"🌐 Opening in browser...")
            print(f"⏹️  Press Ctrl+C to stop the server")
            
            # Open browser
            webbrowser.open(f'http://localhost:{port}')
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n✅ Server stopped successfully!")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use. Trying port {port + 1}...")
            start_server(port + 1)
        else:
            print(f"❌ Error starting server: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_server()