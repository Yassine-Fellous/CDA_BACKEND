# Copyright (c) 2025
# Yassine Fellous, Abdelkader Sofiane Ziri, Mathieu Duverne, Mohamed Marwane Bellagha
# Tous droits réservés. Utilisation interdite sans autorisation écrite des auteurs.
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .models import UserAuth
import secrets
from datetime import timedelta
import json

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        try:
            user = UserAuth.objects.get(email=email)
            if check_password(password, user.password):
                # Génère un token et une date d'expiration
                user.token = secrets.token_hex(32)
                user.token_expire = timezone.now() + timedelta(hours=1)
                user.save()
                return JsonResponse({
                    "token": user.token,
                    "token_expire": user.token_expire,
                    "message": "Connexion réussie"
                })
            else:
                return JsonResponse({"error": "Mot de passe incorrect"}, status=401)
        except UserAuth.DoesNotExist:
            return JsonResponse({"error": "Utilisateur non trouvé"}, status=404)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def register_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return JsonResponse({"error": "Email et mot de passe requis"}, status=400)
        if UserAuth.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email déjà utilisé"}, status=409)
        user = UserAuth.objects.create(
            email=email,
            password=make_password(password)
        )
        return JsonResponse({"message": "Inscription réussie"})
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)