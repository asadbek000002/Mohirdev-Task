import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from intake.models import Lead


@pytest.mark.django_db
def test_create_lead_success_with_file():
    client = APIClient()

    test_file = SimpleUploadedFile(
        "resume.pdf", b"Dummy resume content", content_type="application/pdf"
    )

    payload = {
        "first_name": "Alice",
        "last_name": "Brown",
        "email": "alice@example.com",
        "resume": test_file,
    }

    response = client.post("/intake/lead-create/", data=payload)

    assert response.status_code == 201
    assert Lead.objects.filter(email="alice@example.com").exists()
    assert response.data["first_name"] == "Alice"


@pytest.mark.django_db
def test_create_lead_invalid_data():
    client = APIClient()

    payload = {
        "first_name": "",  # Required field is missing
        "email": "not-an-email",
        # resume yo‘q
    }

    response = client.post("/intake/lead-create/", data=payload)

    assert response.status_code == 400
    assert "first_name" in response.data
    assert "resume" in response.data
