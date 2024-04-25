from Recommender import Recommender
from User import User
from MusicRecommenderSystem import MusicRecommenderSystem
from dotenv import load_dotenv
import os
import base64
from requests import post
import json



class Main:

    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.user = User("user123")  
        self.recommender_system = MusicRecommenderSystem()

    def run(self):
        self.user.load_profile()  # Load user profile at start
        print("Welcome to the Music Recommendation System!")
        while True:
            print("\n1. Add Favorite Track")
            print("2. Get Recommendations")
            print("3. Save and Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                track = input("Enter track name: ")
                self.user.add_favorite_track(track)
            elif choice == '2':
                self.display_recommendations()
            elif choice == '3':
                self.user.save_profile()  # Save profile on exit
                print("Profile saved. Exiting the program.")
                break
            else:
                print("Invalid option. Please try again.")

    def display_recommendations(self):
        favorite_tracks = list(self.user.favorite_tracks)
        if not favorite_tracks:
            print("Please add some favorite tracks first.")
            return
        
        recommendations = self.recommender_system.get_recommendations(favorite_tracks)
        print("Recommendations:")
        for track in recommendations:
            print(track)


    def get_auth_header(token):
        return {"Authorization": "Bearer " + token}

if __name__ == "__main__":
    main_app = Main()
    main_app.run()
