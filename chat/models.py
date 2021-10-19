from django.db import models
from core.models import User
# Create your models here.

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="receiver")
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        ordering = ['id']
        verbose_name = 'User Chat'
        verbose_name_plural = 'User Chats'
        
    def __str__(self):
        return self.message