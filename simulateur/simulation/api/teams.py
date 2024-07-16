from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from simulation.serializers import JoinTeamSerializer, UpdateTeamNameSerializer
from simulation.models import Team, JoinLink, UserProfile
from django.shortcuts import redirect
from rest_framework.views import APIView

@method_decorator(csrf_exempt, name="dispatch")
class JoinTeam(APIView):
    serializer_class = JoinTeamSerializer

    def get(self, request, team_id, key, *args, **kwargs):
        team = get_object_or_404(Team, id=team_id)
        join_link = get_object_or_404(JoinLink, team=team, key=key)

        if join_link.is_expired():
            return Response(
                {"status": "error", "message": "Link has expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return redirect("join_team", team_id=team_id, key=key)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            team_id = serializer.validated_data["team_id"]
            key = serializer.validated_data["key"]
            team = get_object_or_404(Team, id=team_id)
            join_link = get_object_or_404(JoinLink, team=team, key=key)

            if join_link.is_expired():
                return redirect("join_team", error="Link has expired")

            user = request.user
            user_profile = get_object_or_404(UserProfile, user=user)
            if user_profile.team:
                return redirect("team_dashboard", error="You are already part of a team")

            user_profile.team = team
            user_profile.save()
            team.members.add(user_profile)
            return redirect("team_dashboard", success="Successfully joined the team")

        return redirect("join_team", error="Invalid data")

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
