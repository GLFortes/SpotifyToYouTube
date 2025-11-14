#!/usr/bin/env python3
"""Continue adding remaining tracks to an existing YouTube Music playlist"""

import os
import sys
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

load_dotenv()

# Initialize APIs
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
    scope='playlist-read-private playlist-read-collaborative'
))

ytmusic = YTMusic('oauth.json') if os.path.exists('oauth.json') else YTMusic('headers_auth.json')

# Get Spotify playlists
playlists = spotify.current_user_playlists(limit=50)['items']

print("📋 Your Spotify playlists:\n")
for i, pl in enumerate(playlists, 1):
    print(f"  {i}. {pl['name']} ({pl['tracks']['total']} tracks)")

choice = input("\nSelect Spotify playlist number: ").strip()
spotify_playlist = playlists[int(choice) - 1]

print(f"\n📥 Fetching tracks from Spotify playlist: {spotify_playlist['name']}")

# Get all tracks from Spotify
all_tracks = []
results = spotify.playlist_tracks(spotify_playlist['id'])
while results:
    for item in results['items']:
        if item['track']:
            track = item['track']
            all_tracks.append({
                'name': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
            })
    results = spotify.next(results) if results['next'] else None

print(f"   Found {len(all_tracks)} tracks in Spotify")

# Get YouTube Music playlists
yt_playlists = ytmusic.get_library_playlists(limit=50)

print(f"\n📋 Your YouTube Music playlists:\n")
for i, pl in enumerate(yt_playlists, 1):
    print(f"  {i}. {pl['title']} ({pl.get('count', '?')} tracks)")

choice = input("\nSelect YouTube Music playlist number to add to: ").strip()
yt_playlist = yt_playlists[int(choice) - 1]
yt_playlist_id = yt_playlist['playlistId']

print(f"\n📥 Getting current tracks in YouTube Music playlist: {yt_playlist['title']}")

# Get existing tracks in YouTube playlist
existing_playlist = ytmusic.get_playlist(yt_playlist_id, limit=1000)
existing_tracks = set()

if 'tracks' in existing_playlist and existing_playlist['tracks']:
    for track in existing_playlist['tracks']:
        if track:
            track_name = track.get('title', '').lower()
            artists = track.get('artists', [])
            if artists:
                artist_name = artists[0].get('name', '').lower()
                existing_tracks.add(f"{track_name}|{artist_name}")

print(f"   Currently has {len(existing_tracks)} tracks")

# Find tracks that need to be added
print(f"\n🔍 Finding tracks that need to be added...")
tracks_to_add = []

for track in all_tracks:
    track_key = f"{track['name'].lower()}|{track['artist'].split(',')[0].strip().lower()}"
    if track_key not in existing_tracks:
        tracks_to_add.append(track)

print(f"   Need to add {len(tracks_to_add)} more tracks")

if not tracks_to_add:
    print("\n✅ All tracks are already in the playlist!")
    sys.exit(0)

confirm = input(f"\nAdd {len(tracks_to_add)} remaining tracks? (yes/no): ").strip().lower()
if confirm != 'yes':
    print("❌ Cancelled")
    sys.exit(0)

# Search and add remaining tracks
print(f"\n🔍 Searching for tracks on YouTube Music...")
added_count = 0
not_found_count = 0

for i, track in enumerate(tracks_to_add, 1):
    query = f"{track['name']} {track['artist']}"
    print(f"   [{i}/{len(tracks_to_add)}] {track['name']} - {track['artist']}", end="")
    
    try:
        results = ytmusic.search(query, filter='songs', limit=1)
        if results:
            video_id = results[0]['videoId']
            try:
                ytmusic.add_playlist_items(yt_playlist_id, [video_id])
                added_count += 1
                print(" ✓")
            except Exception as e:
                print(f" ✗ Error adding: {str(e)[:30]}")
        else:
            not_found_count += 1
            print(" ✗ Not found")
    except Exception as e:
        print(f" ✗ Search error: {str(e)[:30]}")
    
    # Show progress every 10 tracks
    if i % 10 == 0:
        print(f"   Progress: {added_count} added, {not_found_count} not found")

print(f"\n✅ Done! Added {added_count}/{len(tracks_to_add)} remaining tracks")
print(f"   Total in playlist now: {len(existing_tracks) + added_count} tracks")
