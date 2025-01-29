import numpy as np
from sklearn.neighbors import NearestNeighbors
from django.conf import settings
import joblib

class RecommendationService:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            self.model = joblib.load(settings.ML_MODEL_PATH)
        except:
            # Initialize a new model if none exists
            self.model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')

    def get_recommendations(self, user_id, n_recommendations=5):
        user_data = UserBehavior.objects.filter(user_id=user_id)
        if not user_data.exists():
            return self.get_default_recommendations()
        
        # Transform user data into feature vector
        user_vector = self.prepare_user_vector(user_data)
        
        # Get recommendations using the ML model
        distances, indices = self.model.kneighbors([user_vector])
        return self.get_products_from_indices(indices[0])

    def update_model(self, new_data):
        # Update model with new user behavior data
        self.model.fit(new_data)
        joblib.dump(self.model, settings.ML_MODEL_PATH)