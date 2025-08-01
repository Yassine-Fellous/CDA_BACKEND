# Copyright (c) 2025
# Yassine Fellous, Abdelkader Sofiane Ziri, Mathieu Duverne, Mohamed Marwane Bellagha
# Tous droits réservés. Utilisation interdite sans autorisation écrite des auteurs.

from django.db import models
from django.utils import timezone
from authentication.models import UserAuth
from installations.models import Installation

class Signalement(models.Model):
    message = models.TextField()
    images_url = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=100)
    etat = models.CharField(max_length=100, default='Nouveau')
    utilisateur = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name='signalements')
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, related_name='signalements')

    class Meta:
        db_table = 'signalements'
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'

    def __str__(self):
        return f"{self.type} - {self.etat} ({self.date.date()})"


