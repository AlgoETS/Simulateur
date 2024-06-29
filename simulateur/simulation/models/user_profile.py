from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, blank=True, related_name='user_profiles')
    timestamp = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User Profiles"
