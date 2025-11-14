#!/usr/bin/env python3
"""Helper script to setup YouTube Music authentication using client_secret JSON file"""

import json
import glob
import sys
from ytmusicapi.setup import setup_oauth

# Find the client_secret JSON file
json_files = glob.glob('client_secret_*.json')

if not json_files:
    print("❌ No client_secret JSON file found!")
    print("Please download it from Google Cloud Console and place it in this directory.")
    sys.exit(1)

# Read the JSON file
with open(json_files[0], 'r') as f:
    credentials = json.load(f)

# Extract client_id and client_secret
if 'installed' in credentials:
    client_id = credentials['installed']['client_id']
    client_secret = credentials['installed']['client_secret']
elif 'web' in credentials:
    client_id = credentials['web']['client_id']
    client_secret = credentials['web']['client_secret']
else:
    print("❌ Invalid JSON format!")
    sys.exit(1)

print(f"📝 Found credentials in: {json_files[0]}")
print(f"🔑 Client ID: {client_id[:20]}...")
print(f"\n🌐 Setting up YouTube Music authentication...")
print("A browser window will open. Please authorize the application.\n")

# Setup OAuth with the credentials
try:
    setup_oauth(
        filepath='headers_auth.json',
        client_id=client_id,
        client_secret=client_secret,
        open_browser=True
    )
    print("\n✅ Authentication successful!")
    print("📁 Created: headers_auth.json")
    print("\n🎵 You can now run: python3 spotify_to_youtube.py")
except Exception as e:
    print(f"\n❌ Error during authentication: {e}")
    sys.exit(1)
