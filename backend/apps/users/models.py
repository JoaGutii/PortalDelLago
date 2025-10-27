from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'Superadmin'
        RECEPCION = 'RECEPCION', 'Recepción'
        MUCAMA = 'MUCAMA', 'Mucama'
        MANTENIMIENTO = 'MANTENIMIENTO', 'Mantenimiento'

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.RECEPCION)

    def __str__(self):
        return f"{self.username} ({self.role})"
