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
        installation_id = data.get("installation_id")  # Peut être ID ou inst_numero
        message = data.get("message")
        images_url = data.get("images_url")
        type_ = data.get("type", "Autre")

        if not installation_id or not message:
            return JsonResponse({"error": "installation_id et message requis"}, status=400)

        # ✨ LOGIQUE DE CORRESPONDANCE INTELLIGENTE
        try:
            # Si c'est un nombre, chercher par ID auto-incrémenté
            if str(installation_id).isdigit():
                installation = Installation.objects.get(id=int(installation_id))
            else:
                # Sinon, chercher par inst_numero (ex: "I130010048")
                installation = Installation.objects.get(inst_numero=installation_id)
                
        except Installation.DoesNotExist:
            return JsonResponse({"error": "Installation introuvable"}, status=404)

        signalement = Signalement.objects.create(
            message=message,
            images_url=images_url,
            type=type_,
            utilisateur=user,
            installation=installation,
            date=timezone.now()
        )
        
        return JsonResponse({
            "message": "Signalement créé", 
            "id": signalement.id,
            "installation": {
                "id": installation.id,
                "inst_numero": installation.inst_numero,
                "nom": installation.inst_nom
            }
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
