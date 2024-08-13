from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from simulation.models import Team, JoinLink, UserProfile
from simulation.serializers import JoinTeamSerializer, UpdateTeamNameSerializer


@method_decorator(csrf_exempt, name='dispatch')
class JoinTeam(APIView):
    serializer_class = JoinTeamSerializer

    def get(self, request, team_id, key, *args, **kwargs):
        team = get_object_or_404(Team, id=team_id)
        join_link = get_object_or_404(JoinLink, team=team, key=key)

        if join_link.is_expired():
            messages.error(request, "Link has expired")
            return redirect("join_team")

        return redirect("join_team", team_id=team_id, key=key)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            team_id = serializer.validated_data["team_id"]
            key = serializer.validated_data["key"]
            team = get_object_or_404(Team, id=team_id)
            join_link = get_object_or_404(JoinLink, team=team, key=key)

            if join_link.is_expired():
                messages.error(request, "Link has expired")
                return redirect("join_team")

            user = request.user
            user_profile = get_object_or_404(UserProfile, user=user)
            if user_profile.team:
                messages.error(request, "You are already part of a team")
                return redirect("team_dashboard")

            user_profile.team = team
            user_profile.save()
            team.members.add(user_profile)
            messages.success(request, f"Successfully joined the team {team.name}")
            return redirect("team_dashboard")

        messages.error(request, "Invalid data")
        return redirect("join_team")


class RemoveTeamMember(APIView):
    def post(self, request, team_id, user_id):
        team = get_object_or_404(Team, id=team_id)
        user_to_remove = get_object_or_404(UserProfile, user__id=user_id)

        # Check if the request user is part of the team
        if request.user.userprofile not in team.members.all() and request.user.userprofile.team != team:
            return Response(
                {"status": "error", "message": "You are not a member of this team"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check if the user to remove is a member of the team
        if user_to_remove not in team.members.all():
            return Response(
                {"status": "error", "message": "User is not a member of this team"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Remove the user from the team
        team.members.remove(user_to_remove)
        user_to_remove.team = None
        user_to_remove.save()

        return Response({"status": "success", "message": "User removed from the team"})


class UpdateTeamName(APIView):
    serializer_class = UpdateTeamNameSerializer

    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            team.name = serializer.validated_data["name"]
            team.save()
            return Response(
                {"status": "success", "message": "Team name updated successfully"}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateJoinLink(APIView):
    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)

        if request.user.userprofile not in team.members.all() and request.user.userprofile.team != team:
            return Response(
                {"status": "error", "message": "You are not a member of this team"},
                status=status.HTTP_403_FORBIDDEN,
            )

        join_link = team.generate_join_link()
        join_link_url = f"/join_team/?team_id={team.id}&key={join_link.key}"
        return Response({"status": "success", "join_link": join_link_url})
