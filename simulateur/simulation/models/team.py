from django.db import models
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

class Team(models.Model):
    name = models.CharField(max_length=100, default='')
    members = models.ManyToManyField('UserProfile', related_name='teams')

    def __str__(self):
        return self.name

    def generate_join_link(self):
        unique_key = get_random_string(32)
        join_link = JoinLink.objects.create(
            team=self,
            key=unique_key,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        return join_link.get_absolute_url()

    class Meta:
        verbose_name_plural = "Teams"

class JoinLink(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='join_links')
    key = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def get_absolute_url(self):
        return reverse('join_team', kwargs={'team_id': self.team.id, 'key': self.key})

    class Meta:
        verbose_name_plural = "Join Links"
