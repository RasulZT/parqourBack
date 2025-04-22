from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_fullname', 'role', 'language_code', 'is_staff')
    fieldsets = (
        (None, {
            'fields': (
                'telegram_id', 'telegram_fullname', 'full_name',
                'phone_number', 'language_code', 'role', 'parkings', 'operators'
            )
        }),
    )
    filter_horizontal = ('groups', 'user_permissions', 'parkings', 'operators')
