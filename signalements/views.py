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
    print(f"🔍 DEBUG - Requête reçue: {request.method}")
    
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    user = get_user_from_jwt(request)
    if not user:
        return JsonResponse({"error": "Authentification requise"}, status=401)

    try:
        data = json.loads(request.body)
        installation_id = data.get("installation_id")  # Reçoit "I130010048"
        message = data.get("message")
        images_url = data.get("images_url")
        type_ = data.get("type", "Autre")

        print(f"🔍 DEBUG - installation_id reçu: {installation_id}")

        if not installation_id or not message:
            return JsonResponse({"error": "installation_id et message requis"}, status=400)

        # ✅ TOUJOURS CHERCHER PAR inst_numero (jamais par ID Django)
        try:
            print(f"🔍 DEBUG - Recherche par inst_numero: {installation_id}")
            
            # Ton frontend envoie toujours des inst_numero comme "I130010048"
            installation = Installation.objects.get(inst_numero=installation_id)
            
            print(f"✅ DEBUG - Installation trouvée:")
            print(f"    - ID Django: {installation.id}")
            print(f"    - inst_numero: {installation.inst_numero}")
            print(f"    - Nom: {installation.inst_nom}")
                
        except Installation.DoesNotExist:
            print(f"❌ DEBUG - Installation non trouvée avec inst_numero: {installation_id}")
            return JsonResponse({"error": "Installation introuvable"}, status=404)

        # Créer le signalement avec l'ID Django (foreign key)
        signalement = Signalement.objects.create(
            message=message,
            images_url=images_url,
            type=type_,
            utilisateur=user,
            installation=installation,  # Django utilise automatiquement installation.id
            date=timezone.now()
        )
        
        print(f"✅ DEBUG - Signalement créé:")
        print(f"    - Signalement ID: {signalement.id}")
        print(f"    - Installation FK: {signalement.installation.id}")
        
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
        print(f"❌ DEBUG - Erreur: {str(e)}")
        import traceback
        print(f"❌ DEBUG - Traceback: {traceback.format_exc()}")
        return JsonResponse({"error": str(e)}, status=500)
