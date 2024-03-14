from Recommender import Recommender
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

    def main():
        

        spotify_recommender = Recommender(client_id, client_secret)
        favorite_tracks = []
        print(f"Enter your top %d favorite tracks: ", (track_nums))
        for i in range(track_nums):
            favorite_tracks.append(input(f"Track {i + 1}: "))
        json_file = spotify_recommender.get_json_result(favorite_tracks)

        with open('./result_example.json', 'w') as f:
            json.dump(json_file, f, indent=4)
        
        # favorite_tracks = []
        # print(f"Enter your top %d favorite tracks: ", (track_nums))
        # for i in range(track_nums):
        #     favorite_tracks.append(input(f"Track {i + 1}: "))

        # print("\nRecommendations base on IDs:")
        # recommendation_by_id = spotify_recommender.recommend_tracks_by_id(favorite_tracks)
        # for recommendation in recommendation_by_id:
        #     print(recommendation)

        # print("\nRecommendations based on genres:")
        # recommendations_by_genre = spotify_recommender.recommend_tracks_by_genre(favorite_tracks)
        # for recommendation in recommendations_by_genre:
        #     print(recommendation)

    if __name__ == "__main__":
        main()

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

