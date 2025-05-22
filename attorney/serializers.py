from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from intake.models import Lead
from django.contrib.auth import get_user_model

User = get_user_model()


# Login uchun serializer: username va password orqali token yaratadi
class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user_qidiruv = User.objects.filter(username=username).first()
        if not user_qidiruv:
            raise serializers.ValidationError("User with this username does not exist.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Incorrect password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


# Lead ro'yxatini olish uchun serializer
class LeadsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'resume',
            'status',
            'created_at',
            'updated_at',
        ]


# Lead statusini yangilash uchun serializer
class LeadStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['status']
