from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from simulation.models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        instance.userprofile.save()

@receiver(post_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.delete()
    except UserProfile.DoesNotExist:
        pass

@receiver(user_signed_up)
def social_user_signed_up(request, user, **kwargs):
    UserProfile.objects.get_or_create(user=user)
