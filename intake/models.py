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

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"


class Advertisement(models.Model):
    title = models.CharField(max_length=255)  # Reklama sarlavhasi
    description = models.TextField()  # To‘liq matni
    image = models.ImageField(upload_to='ads/', null=True, blank=True)  # Rasm ixtiyoriy
    is_active = models.BooleanField(default=True)  # Aktivlik
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"

    def __str__(self):
        return self.title
