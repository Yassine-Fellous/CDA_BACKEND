# Copyright (c) 2025
# Yassine Fellous, Abdelkader Sofiane Ziri, Mathieu Duverne, Mohamed Marwane Bellagha
# Tous droits réservés. Utilisation interdite sans autorisation écrite des auteurs.
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from .models import UserAuth
import secrets
from datetime import timedelta, datetime
from django.conf import settings
import jwt
import json
import random
from django.core.mail import send_mail, EmailMultiAlternatives

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        try:
            user = UserAuth.objects.get(email=email)
            if check_password(password, user.password):
                if not user.is_verified:
                    return JsonResponse({'error': 'Compte non validé'}, status=403)
                # Génère un JWT qui expire dans 1h
                expire = datetime.utcnow() + timedelta(hours=1)
                payload = {
                    "email": user.email,
                    "exp": expire
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
                user.token = token
                user.token_expire = expire
                user.save()
                return JsonResponse({
                    "token": token,
                    "token_expire": expire,
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
        code = str(random.randint(100000, 999999))
        user = UserAuth.objects.create(
            email=email,
            password=make_password(password),
            is_verified=False,
            verification_code=code
        )
        html_content = f"""
        <html>
          <body style="background:#f7f9fc;padding:40px;">
            <div style="max-width:400px;margin:auto;background:white;border-radius:12px;box-shadow:0 2px 8px #e3e8ee;padding:32px;">
              <h2 style="color:#2563eb;font-family:sans-serif;">Bienvenue sur <span style="color:#0ea5e9;">SportMap</span> !</h2>
              <p style="font-size:16px;color:#334155;font-family:sans-serif;">
                Voici votre code de validation :
              </p>
              <div style="font-size:32px;font-weight:bold;color:#2563eb;background:#e0f2fe;padding:16px;border-radius:8px;text-align:center;letter-spacing:4px;">
                {code}
              </div>
              <p style="margin-top:24px;font-size:14px;color:#64748b;font-family:sans-serif;">
                <br>
                Merci de votre inscription !
              </p>
            </div>
          </body>
        </html>
        """
        msg = EmailMultiAlternatives(
            'Votre code de validation SportMap',
            f'Votre code est : {code}',
            'noreply@sportmap.me',
            [email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return JsonResponse({"message": "Code envoyé par email"})
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def verify_code_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        code = data.get("code")
        try:
            user = UserAuth.objects.get(email=email)
            if user.verification_code == code:
                user.is_verified = True
                user.verification_code = None
                user.save()
                return JsonResponse({'message': 'Compte validé'})
            else:
                return JsonResponse({'error': 'Code incorrect'}, status=400)
        except UserAuth.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)