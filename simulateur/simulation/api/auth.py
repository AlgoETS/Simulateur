from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from simulation.models import Team, UserProfile
from simulation.serializers import UpdateMemberRoleSerializer


class UpdateMemberRole(generics.GenericAPIView):
    serializer_class = UpdateMemberRoleSerializer

    def post(self, request, team_id, user_id):
        team = get_object_or_404(Team, id=team_id)
        user_profile = get_object_or_404(UserProfile, user__id=user_id)

        # Check if the request user is part of the team
        if request.user.userprofile not in team.members.all():
            return Response({'status': 'error', 'message': 'You are not a member of this team'},
                            status=status.HTTP_403_FORBIDDEN)

        # Check if the user to update is a member of the team
        if user_profile not in team.members.all():
            return Response({'status': 'error', 'message': 'User is not a member of this team'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_profile.role = serializer.validated_data['role']
            user_profile.save()
            return Response({'status': 'success', 'message': 'User role updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
