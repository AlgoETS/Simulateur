import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from simulation.models import UserProfile


class SignupView(View):
    def get(self, request):
        return render(request, "registration/signup.html")

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data["username"]
            email = data["email"]
            password = data["password"]
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            UserProfile.objects.create(user=user)
            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)


class LoginView(View):
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
                return JsonResponse(
                    {"status": "error", "message": "Invalid credentials"}, status=400
                )
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )


class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"status": "success"})


class ProfileView(View):
    def get(self, request):
        # Assuming user is authenticated
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            "user": request.user,
            "user_profile": user_profile,
        }
        return render(request, "registration/profile.html", context)


class SettingsView(View):
    def get(self, request):
        # Assuming user is authenticated
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            "user": request.user,
            "user_profile": user_profile,
        }
        return render(request, "registration/settings.html", context)

    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            user.email = data.get("email", user.email)
            user.save()

            user_profile = UserProfile.objects.get(user=user)
            user_profile.balance = data.get("balance", user_profile.balance)
            user_profile.save()

            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
