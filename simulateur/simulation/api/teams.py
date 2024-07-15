from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import JoinTeamSerializer, UpdateTeamNameSerializer, UpdateMemberRoleSerializer
from .models import JoinLink, Team, UserProfile

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

            user = request.user
            user_profile = get_object_or_404(UserProfile, user=user)
            if user_profile.team:
                return Response({'status': 'error', 'message': 'You are already in a team'}, status=status.HTTP_400_BAD_REQUEST)

            user_profile.team = team
            user_profile.save()
            team.members.add(user_profile)
            return Response({'status': 'success', 'message': f'Joined team {team.name}'})

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

class UpdateTeamName(generics.GenericAPIView):
    serializer_class = UpdateTeamNameSerializer

    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            team.name = serializer.validated_data['name']
            team.save()
            return Response({'status': 'success', 'message': 'Team name updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateMemberRole(generics.GenericAPIView):
    serializer_class = UpdateMemberRoleSerializer

    def post(self, request, team_id, user_id):
        team = get_object_or_404(Team, id=team_id)
        user_profile = get_object_or_404(UserProfile, user__id=user_id)

        # Check if the request user is part of the team
        if request.user.userprofile not in team.members.all():
            return Response({'status': 'error', 'message': 'You are not a member of this team'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the user to update is a member of the team
        if user_profile not in team.members.all():
            return Response({'status': 'error', 'message': 'User is not a member of this team'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_profile.role = serializer.validated_data['role']
            user_profile.save()
            return Response({'status': 'success', 'message': 'User role updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
