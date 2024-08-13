from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

from simulation.models import UserProfile


def admin_required(view_func):
    return user_passes_test(
        lambda user: user.is_superuser, login_url='/admin/login/'
    )(view_func)


def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def team_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        try:
            user_profile = request.user.userprofile
            if not user_profile.id:  # Ensure the UserProfile has been saved
                return JsonResponse({'error': 'User profile does not exist'}, status=403)
            if not user_profile.teams.exists():  # Check if the user is in any team
                return JsonResponse({'error': 'User is not part of a team'}, status=403)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile does not exist'}, status=403)
        return view_func(request, *args, **kwargs)

    return _wrapped_view

