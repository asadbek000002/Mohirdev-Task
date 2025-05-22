from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class EmailErrorLog(models.Model):
    lead_id = models.IntegerField()
    email = models.EmailField()
    error_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Error for Lead ID {self.lead_id} - {self.email}"


class AttorneyEmail(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
