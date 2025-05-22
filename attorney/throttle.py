from rest_framework.throttling import AnonRateThrottle

class LeadCreateThrottle(AnonRateThrottle):
    scope = 'custom_login'
