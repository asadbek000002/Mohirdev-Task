from django.urls import path
from intake.views import LeadCreateApiView, ActiveAdvertisementListView

urlpatterns = [
    path('lead-create/', LeadCreateApiView.as_view(), name='leads_create'),

    path('api/ads/', ActiveAdvertisementListView.as_view()),
]
