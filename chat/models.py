from django.db import models
from core.models import User
from django.utils import timezone
import math, os, uuid, string
from django.core.validators import FileExtensionValidator

# Create your models here.

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_agent', null=True)
    session = models.CharField(max_length=150, unique=True, blank=True)
    is_agent_joined = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Exit Time')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Start Time')

    def save(self, *args, **kwargs):
        u = uuid.uuid4()
        if not self.session:
            self.session = u.hex
        super().save(*args, **kwargs)

    def __str__(self):
        return self.session
    
    class Meta:
        ordering = ['-id']


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

    @property
    def when_sent(self):
        now = timezone.now()
        diff = now - self.sent_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            # return str(seconds) +  "second ago"
            return "few seconds ago"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"


def get_file_path(instance, filename):
    instance_name = instance._meta.model.__name__
    parent_content_name = instance.user.nickname[:15].translate(str.maketrans('', '', string.punctuation)).replace(' ','-').lower()
    upload_to = f'{instance_name.lower()}/{parent_content_name}'
    ext = filename.split('.')[-1]
    # get filename
    gen_filename = filename[:17].replace(ext, '').replace('.', '')
    filename = f"{gen_filename}.{ext}" if instance.pk else f"{uuid.uuid4().hex}.{ext}"
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class ChatTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=get_file_path, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])], help_text='Allowed extensions: png & jpg')
    status = models.BooleanField(default=True)
    use_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    @property
    def ImageUrl(self):
        try:
            url = self.image.url
        except :
            url = ''
        return url