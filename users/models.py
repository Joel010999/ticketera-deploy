from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI")
    full_name = models.CharField(max_length=255, verbose_name="Full Name")

    def __str__(self):
        return f"{self.username} ({self.dni})"
