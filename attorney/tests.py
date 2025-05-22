import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from intake.models import Lead
from django.shortcuts import get_object_or_404
from unittest.mock import patch

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='testpass')


def test_login_success(api_client, test_user):
    response = api_client.post("/attorney/custom-login/", {
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


def test_login_wrong_password(api_client, test_user):
    response = api_client.post("/attorney/custom-login/", {
        "username": "testuser",
        "password": "wrongpass"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.fixture
def client_with_auth_user(db):
    user = User.objects.create_user(username="testuser", password="testpass")
    client = APIClient()
    login_response = client.post("/attorney/custom-login/", {
        "username": "testuser",
        "password": "testpass"
    })
    token = login_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def sample_leads(db):
    lead1 = Lead.objects.create(first_name="Alice", last_name="Smith", email="a@example.com", status="PENDING")
    lead2 = Lead.objects.create(first_name="Bob", last_name="Jones", email="b@example.com", status="REACHED_OUT")
    return lead1, lead2


def test_list_all_leads(client_with_auth_user, sample_leads):
    response = client_with_auth_user.get("/attorney/leads-list/")
    assert response.status_code == 200
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2


def test_filter_leads_by_status(client_with_auth_user, sample_leads):
    response = client_with_auth_user.get("/attorney/leads-list/?status=PENDING")
    assert response.status_code == 200
    assert all(lead["status"] == "PENDING" for lead in response.data["results"])


@patch("intake.tasks.lead_email_task.delay")
def test_patch_lead_status(mock_task, client_with_auth_user, sample_leads):
    lead = sample_leads[0]
    response = client_with_auth_user.patch(f"/attorney/leads-status-update/{lead.id}/")
    assert response.status_code == 200
    assert response.data["status"] == "REACHED_OUT"
    lead.refresh_from_db()
    assert lead.status == Lead.LeadStatus.REACHED_OUT
    mock_task.assert_called_once()


def test_patch_lead_status_already_reached_out(client_with_auth_user, sample_leads):
    lead = sample_leads[1]
    response = client_with_auth_user.patch(f"/attorney/leads-status-update/{lead.id}/")
    assert response.status_code == 400
    assert "already marked" in response.data["detail"]
