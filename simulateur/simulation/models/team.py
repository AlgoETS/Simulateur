from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string


class Team(models.Model):
    name = models.CharField(max_length=100, default='')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def generate_join_link(self):
        unique_key = get_random_string(32)
        join_link = JoinLink.objects.create(
            team=self,
            key=unique_key,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        return join_link

    class Meta:
        verbose_name_plural = "Teams"


class JoinLink(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='join_links')
    key = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Join link for {self.team.name} {self.key}"

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
