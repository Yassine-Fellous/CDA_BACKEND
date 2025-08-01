# Copyright (c) 2025
# Yassine Fellous, Abdelkader Sofiane Ziri, Mathieu Duverne, Mohamed Marwane Bellagha
# Tous droits réservés. Utilisation interdite sans autorisation écrite des auteurs.

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
import jwt
import json

from .models import Signalement
from authentication.models import UserAuth
from installations.models import Installation

def get_user_from_jwt(request):
    auth = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth.split(' ')[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get('email')
        return UserAuth.objects.get(email=email)
    except Exception:
        return None

@csrf_exempt
def create_signalement(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    user = get_user_from_jwt(request)
    if not user:
        return JsonResponse({"error": "Authentification requise"}, status=401)

    try:
        data = json.loads(request.body)
        installation_id = data.get("installation_id")
        message = data.get("message")
        images_url = data.get("images_url")
        type_ = data.get("type", "Autre")

        if not installation_id or not message:
            return JsonResponse({"error": "installation_id et message requis"}, status=400)

        installation = Installation.objects.get(id=installation_id)

        signalement = Signalement.objects.create(
            message=message,
            images_url=images_url,
            type=type_,
            utilisateur=user,
            installation=installation,
            date=timezone.now()
        )
        return JsonResponse({"message": "Signalement créé", "id": signalement.id})
    except Installation.DoesNotExist:
        return JsonResponse({"error": "Installation introuvable"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
