from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login

from simulation.models import JoinLink, Team, UserProfile

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return Response({'status': 'error', 'message': 'Invalid data'}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        return Response({'status': 'success'})

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return Response({'status': 'error', 'message': 'Invalid data'}, status=400)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'status': 'success'})
        return Response({'status': 'error', 'message': 'Invalid credentials'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class JoinTeamView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        team_id = kwargs.get('team_id')
        key = kwargs.get('key')
        team = get_object_or_404(Team, id=team_id)
        join_link = get_object_or_404(JoinLink, team=team, key=key)

        if join_link.is_expired():
            return Response({'status': 'error', 'message': 'Link has expired'}, status=400)

        if team.members.count() == 0:
            user = request.user
            user_profile = get_object_or_404(UserProfile, user=user)
            user_profile.team = team
            user_profile.save()
            team.members.add(user_profile)
            return Response({'status': 'success', 'message': f'Joined team {team.name}'})
        return Response({'status': 'error', 'message': 'Team already has members'}, status=400)
