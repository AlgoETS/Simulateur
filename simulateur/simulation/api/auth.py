from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from simulation.models import JoinLink, Team, UserProfile

@method_decorator(csrf_exempt, name='dispatch')
class JoinTeam(generics.GenericAPIView):
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
