from base64 import urlsafe_b64decode
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from simulation.models.team import JoinLink, Team
from simulation.models.user_profile import UserProfile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings

from simulation.models import UserProfile, Portfolio

CACHE_TTL = getattr(settings, 'CACHE_TTL', 30)



@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    @method_decorator(cache_page(CACHE_TTL), name='dispatch')
    def get(self, request):
        return render(request, "registration/signup.html")

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not username or not email or not password:
                return JsonResponse({"status": "error", "message": "Missing fields"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"status": "error", "message": "Username already exists"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"status": "error", "message": "Email already registered"}, status=400)

            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    @method_decorator(cache_page(CACHE_TTL), name='dispatch')
    def get(self, request):
        return render(request, "registration/login.html")

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data["username"]
            password = data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "Invalid credentials"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

    def post(self, request):
        logout(request)
        return JsonResponse({"status": "success"})

class PublicProfileView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, user_id):
        user_profile = get_object_or_404(UserProfile, user__id=user_id)
        portfolio = get_object_or_404(Portfolio, owner=user_profile)
        context = {
            "user_profile": user_profile,
            "portfolio": portfolio,
        }
        return render(request, "profile/profile.html", context)

class SettingsView(View):
    @method_decorator(login_required)
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        portfolio = get_object_or_404(Portfolio, owner=user_profile)
        context = {
            "user_profile": user_profile,
            "portfolio": portfolio,
        }
        return render(request, "registration/settings.html", context)

    @method_decorator(login_required)
    def post(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        portfolio = get_object_or_404(Portfolio, owner=user_profile)
        if 'avatar' in request.FILES:
            user_profile.avatar = request.FILES['avatar']
        if 'email' in request.POST:
            request.user.email = request.POST['email']
            request.user.save()
        if 'balance' in request.POST:
            portfolio.balance = request.POST['balance']
            portfolio.save()
        return redirect('settings')

class PrivateProfileView(View):
    @method_decorator(login_required)
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        portfolio = get_object_or_404(Portfolio, owner=user_profile)
        context = {
            "user_profile": user_profile,
            "portfolio": portfolio,
        }
        return render(request, "profile/profile.html", context)

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'registration/forgot_password.html')

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'
            )
            mail_subject = 'Reset your password'
            message = render_to_string('registration/email/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            send_mail(mail_subject, message, 'admin@example.com', [email])
            return JsonResponse({"status": "success", "message": "Password reset link sent to your email"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Email not registered"}, status=400)

class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_b64decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            context = {
                'uidb64': uidb64,
                'token': token
            }
            return render(request, 'registration/password_reset_confirm.html', context)
        else:
            return JsonResponse({"status": "error", "message": "Invalid link"}, status=400)

    def post(self, request, uidb64, token):
        try:
            data = json.loads(request.body)
            password = data.get("password")
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return JsonResponse({"status": "success", "message": "Password reset successful"})
            else:
                return JsonResponse({"status": "error", "message": "Invalid link"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class JoinTeamView(View):
    @method_decorator(cache_page(CACHE_TTL), name='dispatch')
    def get(self, request, *args, **kwargs):
        teams = Team.objects.all()
        team_id = request.GET.get('team_id', '')
        key = request.GET.get('key', '')
        teams_balance = [
            {
                'team': team,
                'balance': sum([member.portfolio.balance for member in team.members.all()])
            }
            for team in teams
        ]
        context = {
            'teams': teams,
            'team_id': team_id,
            'key': key,
            'teams_balance': teams_balance
        }
        return render(request, "registration/join_team.html", context)

    def post(self, request, *args, **kwargs):
        team_id = request.POST.get('team_id')
        key = request.POST.get('key')
        team = get_object_or_404(Team, id=team_id)
        join_link = get_object_or_404(JoinLink, team=team, key=key)

        if join_link.is_expired():
            return JsonResponse({'status': 'error', 'message': 'Link has expired'}, status=400)

        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        if user_profile.team:
            return JsonResponse({'status': 'error', 'message': 'You are already in a team'}, status=400)

        user_profile.team = team
        user_profile.save()
        team.members.add(user_profile)
        return JsonResponse({'status': 'success', 'message': f'Joined team {team.name}'})