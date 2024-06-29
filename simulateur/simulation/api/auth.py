from django.shortcuts import get_object_or_404
<<<<<<< HEAD
from rest_framework import generics, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from simulation.serializers import JoinTeamSerializer
from simulation.models import JoinLink, Team, UserProfile

@method_decorator(csrf_exempt, name='dispatch')
class JoinTeam(generics.GenericAPIView):
    serializer_class = JoinTeamSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            team_id = serializer.validated_data['team_id']
            key = serializer.validated_data['key']
            team = get_object_or_404(Team, id=team_id)
            join_link = get_object_or_404(JoinLink, team=team, key=key)

            if join_link.is_expired():
                return Response({'status': 'error', 'message': 'Link has expired'}, status=status.HTTP_400_BAD_REQUEST)

            if team.members.count() == 0:
                user = request.user
                user_profile = get_object_or_404(UserProfile, user=user)
                user_profile.team = team
                user_profile.save()
                team.members.add(user_profile)
                return Response({'status': 'success', 'message': f'Joined team {team.name}'})
            return Response({'status': 'error', 'message': 'Team already has members'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveTeamMember(generics.GenericAPIView):
    def post(self, request, team_id, user_id):
        team = get_object_or_404(Team, id=team_id)
        user_to_remove = get_object_or_404(UserProfile, user__id=user_id)

        # Check if the request user is part of the team
        if request.user.userprofile not in team.members.all():
            return Response({'status': 'error', 'message': 'You are not a member of this team'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the user to remove is a member of the team
        if user_to_remove not in team.members.all():
            return Response({'status': 'error', 'message': 'User is not a member of this team'}, status=status.HTTP_404_NOT_FOUND)

        # Remove the user from the team
        team.members.remove(user_to_remove)
        user_to_remove.team = None
        user_to_remove.save()

        return Response({'status': 'success', 'message': 'User removed from the team'})
=======
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
>>>>>>> origin/main
