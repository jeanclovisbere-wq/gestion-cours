from django.db import models

class Cours(models.Model):
    titre = models.CharField(max_length=200)
    enseignant = models.CharField(max_length=100)
    date_publication = models.DateField()

    def __str__(self):
        return self.titre