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
    print(f"🔍 DEBUG - Utilisateur: {user}")
    
    if not user:
        return JsonResponse({"error": "Authentification requise"}, status=401)

    try:
        data = json.loads(request.body)
        print(f"🔍 DEBUG - Données reçues: {data}")
        
        installation_id = data.get("installation_id")
        message = data.get("message")
        images_url = data.get("images_url")
        type_ = data.get("type", "Autre")

        print(f"🔍 DEBUG - installation_id: {installation_id} (type: {type(installation_id)})")
        print(f"🔍 DEBUG - message: {message}")
        print(f"🔍 DEBUG - type: {type_}")

        if not installation_id or not message:
            return JsonResponse({"error": "installation_id et message requis"}, status=400)

        # ✨ LOGIQUE DE CORRESPONDANCE INTELLIGENTE
        try:
            print(f"🔍 DEBUG - Recherche installation avec: {installation_id}")
            
            # Si c'est un nombre, chercher par ID auto-incrémenté
            if str(installation_id).isdigit():
                print(f"🔍 DEBUG - Recherche par ID numérique: {installation_id}")
                installation = Installation.objects.get(id=int(installation_id))
            else:
                print(f"🔍 DEBUG - Recherche par inst_numero: {installation_id}")
                installation = Installation.objects.get(inst_numero=installation_id)
                
            print(f"✅ DEBUG - Installation trouvée: {installation.id} - {installation.inst_nom}")
                
        except Installation.DoesNotExist:
            print(f"❌ DEBUG - Installation non trouvée: {installation_id}")
            return JsonResponse({"error": "Installation introuvable"}, status=404)

        print(f"🔍 DEBUG - Création du signalement...")
        signalement = Signalement.objects.create(
            message=message,
            images_url=images_url,
            type=type_,
            utilisateur=user,
            installation=installation,
            date=timezone.now()
        )
        
        print(f"✅ DEBUG - Signalement créé: {signalement.id}")
        
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
        print(f"❌ DEBUG - Type d'erreur: {type(e)}")
        import traceback
        print(f"❌ DEBUG - Traceback: {traceback.format_exc()}")
        return JsonResponse({"error": str(e)}, status=500)
