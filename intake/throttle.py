from rest_framework.throttling import AnonRateThrottle

class LeadCreateThrottle(AnonRateThrottle):
    scope = 'lead_create'
