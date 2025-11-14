#!/usr/bin/env python3
"""Test adding tracks to existing YouTube Music playlist"""

from ytmusicapi import YTMusic

try:
    print("🔍 Testing YouTube Music track addition...")
    ytmusic = YTMusic('headers_auth.json')
    
    # The playlist ID from the previous creation
    playlist_id = "PLlz4uPFIo7lpNoxZu7nWEGoR4eyd4fHm2"
    
    print(f"📋 Using playlist ID: {playlist_id}")
    
    # Search for a test song
    print("\n🔍 Searching for test song: 'Breakthrough by TWICE'")
    results = ytmusic.search("Breakthrough TWICE", filter='songs', limit=1)
    
    if results:
        video_id = results[0]['videoId']
        print(f"✅ Found song with video ID: {video_id}")
        
        # Try to add it to the playlist
        print(f"\n➕ Adding track to playlist...")
        try:
            response = ytmusic.add_playlist_items(playlist_id, [video_id])
            print(f"✅ Successfully added! Response: {response}")
        except Exception as e:
            print(f"❌ Failed to add track: {e}")
            print(f"\n💡 Error details: {type(e).__name__}")
    else:
        print("❌ Could not find test song")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
