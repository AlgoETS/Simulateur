from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teams = models.ManyToManyField('Team', blank=True, related_name='user_profiles')
    timestamp = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('member', 'Member'),
            ('team_leader', 'Team Leader'),
            ('admin', 'Admin'),
            ('super_admin', 'Super Admin'),
            ('moderator', 'Moderator')
        ],
        default='member'
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User Profiles"
