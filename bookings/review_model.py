from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    hotel_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    sentiment = models.CharField(max_length=20, null=True, blank=True)
    review_token = models.TextField(null=True, blank=True)
    review_id = models.CharField(max_length=100, null=True, blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'hotel_id']

    def __str__(self):
        return f"Review for Hotel {self.hotel_id} by {self.user.username}"
