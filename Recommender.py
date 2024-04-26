import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict
import numpy as np

class Recommender:
    def __init__(self, client_id, client_secret):
        credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=credentials)

    def get_track_details(self, tracks, market='US'):
        track_details = defaultdict(lambda: {"ids": [], "genres": [], "danceability": [], "energy": []})
        for track in tracks:
            try:
                track_query = self.construct_query(track)
                result = self.sp.search(q=track_query, limit=1, type="track", market=market)
                if result["tracks"]["items"]:
                    item = result["tracks"]["items"][0]
                    track_id = item["id"]
                    features = self.sp.audio_features(track_id)[0]

                    track_details[track]["ids"].append(track_id)
                    track_details[track]["genres"].extend(item["artists"][0].get("genres", []))
                    if features:
                        track_details[track]["danceability"].append(features.get("danceability", 0))
                        track_details[track]["energy"].append(features.get("energy", 0))
            except spotipy.SpotifyException as e:
                print(f"An error occurred while processing track {track}: {str(e)}")
        return track_details

    def recommend_tracks_by_id(self, favorite_tracks, market="US"):
        details = self.get_track_details(favorite_tracks, market)
        track_ids = [d['ids'][0] for d in details.values() if d['ids']]
        recommendations = [] 
        if track_ids:
            recommended = self.sp.recommendations(seed_tracks=track_ids, limit=3)
            for track in recommended['tracks']:
                recommendations.append(f"{track['name']} by {track['artists'][0]['name']}")
        return recommendations if recommendations else ["Sorry, we couldn't find any recommendations."]

    def recommend_tracks_by_genre(self, favorite_tracks, market='US'):
        details = self.get_track_details(favorite_tracks, market)
        genres = {genre for d in details.values() for genre in d['genres'] if d['genres']}
        user_track_names = [track.split(' artist:')[0].lower() for track in favorite_tracks]  # 입력된 트랙 이름 추출
        
        recommendations = []
        if genres:
            try:
                recommended = self.sp.recommendations(seed_genres=list(genres)[:5], limit=5, market=market)
                for track in recommended['tracks']:
                    if track['name'].lower() not in user_track_names:
                        recommendations.append(f"{track['name']} by {track['artists'][0]['name']}")
            except spotipy.SpotifyException as e:
                print(f"Error during genre-based recommendations: {str(e)}")
        return recommendations if recommendations else ["Sorry, no recommendations could be generated."]

    def construct_query(self, track):
        # This method constructs a specific query from the track input
        # Expecting track in the format "track name artist:artist name" if artist is provided
        if " artist:" in track:
            track_name, artist_name = track.split(" artist:")
            return f"track:{track_name} artist:{artist_name}"
        else:
            return f"track:{track}"