# views.py 또는 다른 파일에서 Recommender 모듈 임포트
from .Recommender import Recommender
from dotenv import load_dotenv
import os
import base64
from requests import post
import json

track_nums = 5
load_dotenv()
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

    
class Main:
    def run(self):
        # Collect Spotify API credentials from environment variables
        client_id = os.environ.get("CLIENT_ID")
        client_secret = os.environ.get("CLIENT_SECRET")

        # Initialize the Spotify recommender
        spotify_recommender = Recommender(client_id, client_secret)

        # User inputs
        favorite_tracks = []
        track_count = int(input("How many favorite tracks would you like to input? "))
        market = input("Enter Spotify market (e.g., US, FR, DE; press enter for default 'US'): ")
        market = market if market else 'US'  # Default to US if no input

        for i in range(track_count):
            track_name = input(f"Enter favorite track {i+1} name: ")
            artist_name = input(f"Enter artist for track {i+1} (optional, press enter to skip): ")
            if artist_name:
                track = f"{track_name} artist:{artist_name}"
            else:
                track = track_name
            favorite_tracks.append(track)

        # Get recommendations
        print("\nFinding recommendations based on your favorite tracks...")
        id_recommendations = spotify_recommender.recommend_tracks_by_id(favorite_tracks, market)
        genre_recommendations = spotify_recommender.recommend_tracks_by_genre(favorite_tracks, market)

        # Combine recommendations
        all_recommendations = list(set(id_recommendations + genre_recommendations))
        if len(all_recommendations) > 3:
            all_recommendations = all_recommendations[:3]  # Select top 3 unique recommendations
        elif len(all_recommendations) < 3:
            # If fewer than 3 unique recommendations, attempt to fill from either source
            all_recommendations.extend(id_recommendations if len(id_recommendations) > len(genre_recommendations) else genre_recommendations)
            all_recommendations = list(set(all_recommendations))[:3]  # Ensure no duplicates and only take up to 3

        # Output the final recommendations
        if all_recommendations:
            print("\nRecommended tracks:")
            for recommendation in all_recommendations:
                print(recommendation)
        else:
            print("Sorry, we couldn't find any recommendations.")

    def get_token():
        auth_string = client_id + ":" + client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content_Type": "application/x-www-form-urlcoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

    def get_auth_header(token):
        return {"Authorization": "Bearer " + token}

if __name__ == "__main__":
    main_app = Main()
    main_app.run()