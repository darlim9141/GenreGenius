import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class MusicRecommenderSystem:
    def __init__(self, interaction_matrix):
        self.interaction_matrix = interaction_matrix
        self.similarity_df = self.calculate_similarity()

    def calculate_similarity(self):
        return pd.DataFrame(cosine_similarity(self.interaction_matrix),
                            index=self.interaction_matrix.index,
                            columns=self.interaction_matrix.index)

    def recommend_tracks(self, user_id, top_n=3):
        similar_users = self.similarity_df[user_id].sort_values(ascending=False)[1:]
        recommended_tracks = pd.Series(dtype='float64')
        for other_user, similarity in similar_users.iteritems():
            recommended_tracks = recommended_tracks.add(self.interaction_matrix.loc[other_user] * similarity, fill_value=0)
        already_rated = self.interaction_matrix.loc[user_id] > 0
        recommended_tracks = recommended_tracks[~already_rated]
        return recommended_tracks.sort_values(ascending=False).head(top_n)

    @staticmethod
    def create_interaction_matrix(df, user_col, item_col, rating_col, norm=False):
        interactions = df.pivot(index=user_col, columns=item_col, values=rating_col)
        if norm:
            interactions = interactions.apply(lambda x: (x - x.mean()) / (x.max() - x.min() if (x.max() - x.min()) != 0 else 1), axis=1)
        interactions = interactions.fillna(0)
        return interactions

    def collaborative_filtering(user_id, interaction_matrix):
        # Compute similarities
        similarity_matrix = cosine_similarity(interaction_matrix)
        similarity_df = pd.DataFrame(similarity_matrix, index=interaction_matrix.index, columns=interaction_matrix.index)

        # Get top similar users
        similar_users = similarity_df[user_id].sort_values(ascending=False)[1:4]  # Exclude self
        similar_users = similar_users.index.tolist()

        # Aggregate scores
        recommendations = interaction_matrix.loc[similar_users].mean(axis=0)
        recommendations = recommendations.sort_values(ascending=False)

        return recommendations.to_dict()
    
    def content_based_filtering(user_profile, items_df):
        # Assume items_df contains columns for 'track_id' and 'genre'
        # User profile should contain a favorite genre
        favorite_genre = user_profile.favorite_genre
        recommendations = items_df[items_df['genre'] == favorite_genre]['track_id'].tolist()
        return recommendations
    
    def recommend_by_context(user_profile):
        # Context data might include time_of_day, mood, etc.
        context = user_profile.context
        if context['time_of_day'] == 'evening' and context['mood'] == 'relaxed':
            return ['track2', 'track4']  # IDs of relaxing tracks suitable for evening
        return []
