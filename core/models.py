from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser
import uuid 


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    mobile = models.CharField(max_length=15, verbose_name="Mobile number", null=True, blank=True)
    whatsapp = models.CharField(max_length=15, verbose_name="Whatsapp number", null=True, blank=True)
    is_available = models.BooleanField(default=False)
    

    def save(self, *args, **kwargs):
        if not self.username:
            username = self.email.split('@')[0]
            self.username = f"{username}.{uuid.uuid4().hex[:4]}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def nickname(self):
        if self.first_name:
            return self.first_name
        return self.username
        
    
    