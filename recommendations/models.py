from django.db import models
from django.contrib.auth.models import User

class UserBehavior(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)
    rating = models.IntegerField(null=True, blank=True)