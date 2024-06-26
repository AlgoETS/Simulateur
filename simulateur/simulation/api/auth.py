# simulation/api/auth.py
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login

from simulation.models import UserProfile
from simulation.serializers import UserSerializer, UserProfileSerializer

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        UserProfile.objects.create(user=user)
        return Response({'status': 'success'})

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        user = authenticate(request, username=data['username'], password=data['password'])
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
