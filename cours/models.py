from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

def valider_date(value):
    if value > timezone.now().date():
        raise ValidationError("La date ne peut pas être dans le futur !")

class Cours(models.Model):
    titre = models.CharField(max_length=200)
    enseignant = models.CharField(max_length=100)
    date_publication = models.DateField()

    def clean(self):
        valider_date(self.date_publication)

    def __str__(self):
        return self.titre