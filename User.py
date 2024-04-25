import json

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.favorite_genres = set()
        self.favorite_artists = set()
        self.favorite_tracks = set()
        self.track_feedback = {}
        self.context = {}

    def add_favorite_genre(self, genre):
        self.favorite_genres.add(genre)

    def add_favorite_artist(self, artist):
        self.favorite_artists.add(artist)

    def add_favorite_track(self, track):
        self.favorite_tracks.add(track)

    def save_profile(self):
        profile_data = {
            "Favorite Genres": list(self.favorite_genres),
            "Favorite Artists": list(self.favorite_artists),
            "Favorite Tracks": list(self.favorite_tracks)
        }
        try:
            with open(f"{self.user_id}_profile.json", "w") as file:
                json.dump(profile_data, file)
        except IOError as e:
            print(f"Error saving profile: {e}")

    def load_profile(self):
        try:
            with open(f"{self.user_id}_profile.json", "r") as file:
                data = json.load(file)
                self.favorite_genres = set(data["Favorite Genres"])
                self.favorite_artists = set(data["Favorite Artists"])
                self.favorite_tracks = set(data["Favorite Tracks"])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading profile: {e}, starting with an empty profile.")

    def add_feedback(self, track_id, feedback_type):
        self.track_feedback[track_id] = feedback_type

    def get_feedback(self):
        return self.track_feedback

    @staticmethod
    def simulate_user_interaction(user_profile, track_id, feedback_type):
        user_profile.add_feedback(track_id, feedback_type)

    def update_context(self, context_data):
        self.context = context_data

    @staticmethod
    def set_user_context(user_profile, context_data):
        user_profile.update_context(context_data)


