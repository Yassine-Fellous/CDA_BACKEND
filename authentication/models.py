# Copyright (c) 2025
# Yassine Fellous, Abdelkader Sofiane Ziri, Mathieu Duverne, Mohamed Marwane Bellagha
# Tous droits réservés. Utilisation interdite sans autorisation écrite des auteurs.

from django.db import models
from django.utils import timezone

# Modèle pour l'authentification des utilisateurs
class UserAuth(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=10, null=True, blank=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token_created = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Nouveau champ pour l'administration
    is_admin = models.BooleanField(default=False)  # ← NOUVEAU


    class Meta:
        db_table = 'user_auth'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return self.email