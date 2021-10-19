from django.db import models
from core.models import User
import uuid
# Create your models here.

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_agent', null=True)
    session = models.CharField(max_length=150, unique=True, blank=True)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        u = uuid.uuid4()
        if not self.session:
            self.session = u.hex
        super().save(*args, **kwargs)

    def __str__(self):
        return self.session


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="receiver")
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, null=True)
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


class ChatTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)