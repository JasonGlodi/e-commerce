from django.urls import path
from .views import RecommendationView
urlpatterns = [
    path('recommendations/', RecommendationView.as_view(), name='get_recommendations'),
    path('recommendations/', RealtimeRecommendationView.as_view(), name='realtime_recommendations'),
]

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RealtimeRecommendationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
    async def disconnect(self, close_code):
        pass
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        user_id = data.get('user_id')
        
        # Get real-time recommendations
        recommendations = await self.get_realtime_recommendations(user_id)
        
        # Send recommendations back to the client
        await self.send(text_data=json.dumps({
            'type': 'recommendations',
            'data': recommendations
        }))

    async def get_realtime_recommendations(self, user_id):
        service = RecommendationService()
        return await service.get_recommendations(user_id)