#!/usr/bin/env python3
"""
Spotify to YouTube Music Playlist Transfer
Transfers playlists from Spotify to YouTube Music

SECURITY FEATURES:
- Encrypted token storage using cryptography library
- OS keyring integration for encryption keys
- Minimal OAuth scopes (principle of least privilege)
- Secure file permissions (0600)
- Token validation and revocation checks
"""

import os
import sys
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from security_manager import SecureTokenManager, SecureHeadersManager

# Load environment variables
load_dotenv()


class YouTubeOAuthWrapper:
    """Wrapper to use YouTube API with OAuth (with encryption) and ytmusicapi"""
    
    def __init__(self, token_file='youtube_token.enc'):
        self.token_file = token_file
        self.token_manager = SecureTokenManager(token_file=token_file)
        self.creds = self._load_credentials()
        self.ytmusic = self._init_ytmusic()
        
    def _load_credentials(self):
        """Load and refresh OAuth credentials with security"""
        creds_data = self.token_manager.load_credentials()
        
        if not creds_data:
            raise FileNotFoundError(f"Token criptografado não encontrado: {self.token_file}")
        
        creds = Credentials(
            token=creds_data['token'],
            refresh_token=creds_data['refresh_token'],
            token_uri=creds_data['token_uri'],
            client_id=creds_data['client_id'],
            client_secret=creds_data['client_secret'],
            scopes=creds_data['scopes']
        )
        
        if creds_data.get('expiry'):
            creds.expiry = datetime.fromisoformat(creds_data['expiry'])
        
        # Auto-refresh if expired
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Renovando token automaticamente...")
            try:
                creds.refresh(Request())
                self.token_manager.save_credentials(creds)
                print("✅ Token renovado!")
                
                # Validate token wasn't revoked
                try:
                    test_service = build('youtube', 'v3', credentials=creds)
                    test_service.channels().list(part='snippet', mine=True).execute()
                except HttpError as e:
                    if e.resp.status == 401:
                        print("❌ Token foi revogado! Execute: python3 setup_youtube_oauth.py")
                        sys.exit(1)
                        
            except Exception as e:
                print(f"❌ Erro ao renovar token: {e}")
                print("   Execute: python3 setup_youtube_oauth.py")
                sys.exit(1)
        
        return creds
    
    def _init_ytmusic(self):
        """Initialize ytmusicapi with secure headers (fallback for search)"""
        headers_manager = SecureHeadersManager()
        headers = headers_manager.load_headers()
        
        if headers:
            return YTMusic(auth=headers)
        
        # Try legacy unencrypted file
        legacy_file = 'headers_auth.json'
        if os.path.exists(legacy_file):
            print("⚠️  Encontrado arquivo headers não criptografado, migrando...")
            import json
            with open(legacy_file, 'r') as f:
                headers = json.load(f)
            headers_manager.save_headers(headers)
            os.remove(legacy_file)
            return YTMusic(auth=headers)
        
        return None
    
    def search(self, query: str, filter: str = None, limit: int = 1):
        """Search using ytmusicapi"""
        if not self.ytmusic:
            raise Exception("YTMusic not initialized. Run: python3 setup_youtube_headers.py")
        return self.ytmusic.search(query, filter=filter, limit=limit)
    
    def create_playlist(self, title: str, description: str = "", privacy_status: str = "PRIVATE"):
        """Create playlist using OAuth"""
        youtube = build('youtube', 'v3', credentials=self.creds)
        
        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": privacy_status
                }
            }
        )
        response = request.execute()
        return response['id']
    
    def add_playlist_item(self, playlist_id: str, video_id: str):
        """Add video to playlist using OAuth"""
        youtube = build('youtube', 'v3', credentials=self.creds)
        
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        response = request.execute()
        return response


class SpotifyToYouTubeTransfer:
    """Main class for transferring playlists from Spotify to YouTube Music"""
    
    def __init__(self):
        """Initialize the transfer tool with authentication"""
        self.spotify = self._authenticate_spotify()
        self.ytmusic = self._authenticate_youtube()
        
    def _authenticate_spotify(self) -> spotipy.Spotify:
        """Authenticate with Spotify API"""
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        
        if not all([client_id, client_secret, redirect_uri]):
            raise ValueError(
                "Missing Spotify credentials. Please set SPOTIFY_CLIENT_ID, "
                "SPOTIFY_CLIENT_SECRET, and SPOTIFY_REDIRECT_URI in .env file"
            )
        
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope='playlist-read-private playlist-read-collaborative'
        )
        
        return spotipy.Spotify(auth_manager=auth_manager)
    
    def _authenticate_youtube(self):
        """Authenticate with YouTube Music API using secure OAuth with auto-refresh"""
        token_file = 'youtube_token.enc'
        
        if not os.path.exists(token_file):
            print(f"\n❌ Token criptografado não encontrado!")
            print(f"\n🔐 Execute primeiro:")
            print(f"  python3 setup_youtube_oauth.py")
            sys.exit(1)
        
        try:
            return YouTubeOAuthWrapper(token_file)
        except Exception as e:
            print(f"❌ Erro na autenticação OAuth: {e}")
            print(f"\n🔐 Tente reconfigurar:")
            print(f"  python3 setup_youtube_oauth.py")
            print(f"  python3 setup_youtube_headers.py  # Para buscas")
            sys.exit(1)
    
    def get_spotify_playlists(self) -> List[Dict]:
        """Get all user's Spotify playlists"""
        playlists = []
        results = self.spotify.current_user_playlists(limit=50)
        
        while results:
            playlists.extend(results['items'])
            if results['next']:
                results = self.spotify.next(results)
            else:
                results = None
        
        return playlists
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """Get all tracks from a Spotify playlist"""
        tracks = []
        results = self.spotify.playlist_tracks(playlist_id)
        
        while results:
            for item in results['items']:
                if item['track']:
                    track = item['track']
                    tracks.append({
                        'name': track['name'],
                        'artist': ', '.join([artist['name'] for artist in track['artists']]),
                        'album': track['album']['name']
                    })
            
            if results['next']:
                results = self.spotify.next(results)
            else:
                results = None
        
        return tracks
    
    def search_youtube_track(self, track_name: str, artist: str) -> Optional[str]:
        """Search for a track on YouTube Music"""
        query = f"{track_name} {artist}"
        try:
            results = self.ytmusic.search(query, filter='songs', limit=5)
            
            if results:
                # Return the video ID of the first result
                return results[0]['videoId']
            
        except Exception as e:
            print(f"  ⚠️  Error searching for '{query}': {e}")
        
        return None
    
    def create_youtube_playlist(self, title: str, description: str = "") -> str:
        """Create a new playlist on YouTube Music"""
        playlist_id = self.ytmusic.create_playlist(
            title=title,
            description=description or f"Transferred from Spotify",
            privacy_status="PRIVATE"
        )
        return playlist_id
    
    def add_tracks_to_youtube_playlist(self, playlist_id: str, video_ids: List[str]) -> int:
        """Add tracks to a YouTube Music playlist one by one"""
        added_count = 0
        failed_count = 0
        
        for i, video_id in enumerate(video_ids, 1):
            try:
                self.ytmusic.add_playlist_item(playlist_id, video_id)
                added_count += 1
                if i % 10 == 0 or i == len(video_ids):
                    print(f"   Progress: {added_count}/{len(video_ids)} tracks added...")
            except Exception as e:
                failed_count += 1
                if failed_count <= 3:  # Only show first 3 errors
                    print(f"  ⚠️  Failed to add track {i}: {str(e)[:50]}")
        
        return added_count
    
    def transfer_playlist(self, spotify_playlist_id: str, spotify_playlist_name: str) -> None:
        """Transfer a complete playlist from Spotify to YouTube Music"""
        print(f"\n🎵 Transferring playlist: {spotify_playlist_name}")
        print("=" * 60)
        
        # Get tracks from Spotify
        print("📥 Fetching tracks from Spotify...")
        tracks = self.get_playlist_tracks(spotify_playlist_id)
        print(f"   Found {len(tracks)} tracks")
        
        # Create YouTube Music playlist
        print("📤 Creating YouTube Music playlist...")
        yt_playlist_id = self.create_youtube_playlist(
            title=spotify_playlist_name,
            description=f"Transferred from Spotify - {len(tracks)} tracks"
        )
        print(f"   Created playlist ID: {yt_playlist_id}")
        
        # Search and add tracks
        print("🔍 Searching for tracks on YouTube Music...")
        video_ids = []
        found_count = 0
        
        for i, track in enumerate(tracks, 1):
            print(f"   [{i}/{len(tracks)}] {track['name']} - {track['artist']}", end="")
            video_id = self.search_youtube_track(track['name'], track['artist'])
            
            if video_id:
                video_ids.append(video_id)
                found_count += 1
                print(" ✓")
            else:
                print(" ✗ Not found")
        
        # Add all found tracks to the playlist
        if video_ids:
            print(f"\n➕ Adding {len(video_ids)} tracks to YouTube Music playlist...")
            added_count = self.add_tracks_to_youtube_playlist(yt_playlist_id, video_ids)
            
            if added_count > 0:
                print(f"✅ Successfully added {added_count}/{len(video_ids)} tracks to the playlist!")
            else:
                print(f"❌ Failed to add tracks to the playlist")
        else:
            print("\n❌ No tracks found on YouTube Music")
        
        print("\n" + "=" * 60)
    
    def interactive_transfer(self) -> None:
        """Interactive mode to select and transfer playlists"""
        print("\n" + "=" * 60)
        print("🎵 Spotify to YouTube Music Transfer Tool")
        print("=" * 60)
        
        # Get user's playlists
        print("\n📋 Fetching your Spotify playlists...")
        playlists = self.get_spotify_playlists()
        
        if not playlists:
            print("❌ No playlists found!")
            return
        
        # Display playlists
        print(f"\nFound {len(playlists)} playlists:\n")
        for i, playlist in enumerate(playlists, 1):
            track_count = playlist['tracks']['total']
            print(f"  {i}. {playlist['name']} ({track_count} tracks)")
        
        # Get user selection
        print("\nOptions:")
        print("  - Enter playlist number to transfer")
        print("  - Enter 'all' to transfer all playlists")
        print("  - Enter 'q' to quit")
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            print("👋 Goodbye!")
            return
        
        if choice == 'all':
            confirm = input(f"\n⚠️  Transfer all {len(playlists)} playlists? (yes/no): ").strip().lower()
            if confirm == 'yes':
                for playlist in playlists:
                    self.transfer_playlist(playlist['id'], playlist['name'])
            else:
                print("❌ Transfer cancelled")
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(playlists):
                    playlist = playlists[index]
                    self.transfer_playlist(playlist['id'], playlist['name'])
                else:
                    print("❌ Invalid playlist number!")
            except ValueError:
                print("❌ Invalid input!")


def main():
    """Main entry point"""
    try:
        transfer = SpotifyToYouTubeTransfer()
        transfer.interactive_transfer()
    except KeyboardInterrupt:
        print("\n\n👋 Transfer cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
