from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Review(models.Model):
    hotel_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    sentiment = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for Hotel {self.hotel_id} by {self.user.username}"

    def get_sentiment(self):
        """Basic sentiment based on rating"""
        if self.rating >= 4:
            return "positive"
        elif self.rating <= 2:
            return "negative"
        else:
            return "neutral"