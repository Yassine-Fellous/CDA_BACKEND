# Copyright (c) 2025
# Yassine Fellous, Abdelkader Sofiane Ziri, Mathieu Duverne, Mohamed Marwane Bellagha
# Tous droits réservés. Utilisation interdite sans autorisation écrite des auteurs.

from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class UserAuth(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Stocke le hash, pas le mot de passe en clair
    token = models.CharField(max_length=64, blank=True, null=True)
    token_expire = models.DateTimeField(blank=True, null=True)

    def is_token_valid(self):
        return self.token and self.token_expire and self.token_expire > timezone.now()

    def __str__(self):
        return self.email