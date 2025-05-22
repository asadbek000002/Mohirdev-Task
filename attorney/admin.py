from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User, EmailErrorLog, AttorneyEmail


class UserAdmin(BaseUserAdmin):
    # Admin panelda ko'rinadigan maydonlar
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)



class EmailErrorLogAdmin(admin.ModelAdmin):
    list_display = ('lead_id', 'email', 'error_message', 'created_at')
    readonly_fields = ('lead_id', 'email', 'error_message', 'created_at')


class AttorneyEmailAdmin(admin.ModelAdmin):
    list_display = ["email"]


admin.site.register(User, UserAdmin)
admin.site.register(EmailErrorLog, EmailErrorLogAdmin)
admin.site.register(AttorneyEmail, AttorneyEmailAdmin)
admin.site.unregister(Group)
