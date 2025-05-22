from django.contrib import admin
from .models import Lead, Advertisement


class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'start_date', 'end_date', 'created_at')  # Admin ro'yxat ko‘rinishi
    list_filter = ('is_active', 'start_date', 'end_date')  # Yon panelda filterlar
    search_fields = ('title', 'description')  # Qidiruv maydoni
    readonly_fields = ('created_at',)  # O‘zgartirib bo‘lmaydigan maydon
    ordering = ('-created_at',)  # Eng yangi reklamalar yuqorida chiqadi


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Lead, LeadAdmin)
