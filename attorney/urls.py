from django.urls import path
from attorney.views import CustomLoginView, LeadsListApiView, LeadStatusUpdateAPIView, lead_statistics, CustomLogoutView

urlpatterns = [
    path('custom-login/', CustomLoginView.as_view(), name='custom_login'),
    path('custom-logout/', CustomLogoutView.as_view(), name='custom_logout'),

    path('leads/statistics/', lead_statistics, name='lead-statistics'),
    path('leads-list/', LeadsListApiView.as_view(), name='leads_list'),
    path('leads-status-update/<int:pk>/', LeadStatusUpdateAPIView.as_view(), name='leads_status_update'),

]
