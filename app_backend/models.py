from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    # bio = models.TextField(null=True, blank=True)
    first_name = models.TextField(default='')
    last_name = models.TextField(default='')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default='')
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile} - {self.created_at}'




