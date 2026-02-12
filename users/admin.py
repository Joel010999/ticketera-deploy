from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'full_name', 'dni', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('dni', 'full_name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('dni', 'full_name')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
