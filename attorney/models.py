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

    class Meta:
        verbose_name = "EmailErrorLog"
        verbose_name_plural = "Email Error Logs"

    def __str__(self):
        return f"Error for Lead ID {self.lead_id} - {self.email}"


class AttorneyEmail(models.Model):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Attorney Email"
        verbose_name_plural = "Attorney Emails"

    def __str__(self):
        return self.email
