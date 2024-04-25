import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict

class Recommender:
    def __init__(self, client_id, client_secret):
        credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=credentials)

    def get_track_details(self, tracks):
        track_details = defaultdict(lambda: {"ids": [], "genres": []})
        for track in tracks:
            result = self.sp.search(q=track, limit=1, type="track")
            if result["tracks"]["items"]:
                item = result["tracks"]["items"][0]
                track_id = item["id"]
                artist_id = item["artists"][0]["id"]
                artist = self.sp.artist(artist_id)
                genres = artist['genres']
                
                track_details[track]["ids"].append(track_id)
                track_details[track]["genres"].extend(genres)
        return track_details
    
    def recommend_tracks_by_id(self, favorite_tracks):
        details = self.get_track_details(favorite_tracks)
        track_ids = [d['ids'][0] for d in details.values() if d['ids']]
        recommendations = []
        if track_ids:
            recommended = self.sp.recommendations(seed_tracks=track_ids, limit=3)
            for track in recommended['tracks']:
                recommendations.append(f"{track['name']} by {track['artists'][0]['name']}")
        return recommendations if recommendations else ["Sorry, we couldn't find any recommendations."]
        
    def recommend_tracks_by_genre(self, favorite_tracks):
        details = self.get_track_details(favorite_tracks)
        genres = {genre for d in details.values() for genre in d['genres'] if d['genres']}
        recommendations = []
        if genres:
            recommended = self.sp.recommendations(seed_genres=list(genres)[:5], limit=3)
            for track in recommended['tracks']:
                recommendations.append(f"{track['name']} by {track['artists'][0]['name']}")
        return recommendations if recommendations else ["Sorry, we couldn't find any recommendations."]

    def get_available_genre_seeds(self):
        genres = self.sp.recommendation_genre_seeds()
        return genres
    
    def get_json_result(self, favorite_tracks):
        details = self.get_track_details(favorite_tracks)
        track_ids = [d['ids'][0] for d in details.values() if d['ids']]
        recommended = self.sp.recommendations(seed_tracks=track_ids, limit=50)
        return recommended
    
    def get_track_info(self, track_ids):
        tracks_info = []
        for track_id in track_ids:
            track_data = self.sp.track(track_id)
            audio_features = self.sp.audio_features(track_id)[0]

            track_info = {
                'id': track_id,
                'name': track_data['name'],
                'artist': track_data['artists'][0]['name'],
                'album': track_data['album']['name'],
                'release_date': track_data['album']['release_date'],
                'popularity': track_data['popularity'],
                'duration_ms': track_data['duration_ms'],
                'explicit': track_data['explicit'],
                # Audio features
                'danceability': audio_features['danceability'],
                'energy': audio_features['energy'],
                'key': audio_features['key'],
                'loudness': audio_features['loudness'],
                'mode': audio_features['mode'],
                'speechiness': audio_features['speechiness'],
                'acousticness': audio_features['acousticness'],
                'instrumentalness': audio_features['instrumentalness'],
                'liveness': audio_features['liveness'],
                'valence': audio_features['valence'],
                'tempo': audio_features['tempo'],
                'time_signature': audio_features['time_signature']
            }
            tracks_info.append(track_info)
        return tracks_info
    

    def get_track_ids(self, track_names):
        track_ids = []
        for track_name in track_names:
            result = self.sp.search(q=track_name, limit=1, type='track')
            if result['tracks']['items']:
                track_id = result['tracks']['items'][0]['id']
                track_ids.append(track_id)
        return track_ids
    
    def clean_data(data):
        # Remove duplicates
        data = data.drop_duplicates()

        # Fill or drop missing values
        data['genre'] = data['genre'].fillna('Unknown')  # Fill missing genres with 'Unknown'
        data.dropna(subset=['artist', 'track_name'], inplace=True)  # Drop rows where 'artist' or 'track_name' is missing

        return data
