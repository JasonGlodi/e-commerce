from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from services import RecommendationService

class RecommendationView(APIView):
    def __init__(self):
        super().__init__()
        self.recommendation_service = RecommendationService

    def get(self, request):
        user_id = request.user.id
        n_recommendations = request.query_params.get('count', 5)
        
        recommendations = self.recommendation_service.get_recommendations(
            user_id, 
            n_recommendations=int(n_recommendations)
        )
        
        return Response(recommendations, status=status.HTTP_200_OK)