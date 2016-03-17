from django.db import models


class Race(models.Model):
    name = models.CharField(max_length=255, unique=True)
    date = models.DateField()
