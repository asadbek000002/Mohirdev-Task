from django.db import models


class Lead(models.Model):
    class LeadStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        REACHED_OUT = "REACHED_OUT", "Reached Out"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"
