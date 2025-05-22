from rest_framework import serializers
from .models import Lead
import os

# Lead ro'yxatini yaratish uchun serializer
class LeadSerializer(serializers.ModelSerializer):
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
        read_only_fields = ['status', 'created_at', 'updated_at']

    def validate_resume(self, value):
        max_size = 10 * 1024 * 1024  # 10 MB
        allowed_extensions = ['.pdf', '.doc', '.docx']

        if value.size > max_size:
            raise serializers.ValidationError("The file size should not exceed 10MB.")

        ext = os.path.splitext(value.name)[1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError("Only .pdf, .doc, .docx files are accepted.")

        return value
