from django.urls import path
from intake.views import LeadCreateApiView

urlpatterns = [
    path('lead-create/', LeadCreateApiView.as_view(), name='leads_create'),
]
