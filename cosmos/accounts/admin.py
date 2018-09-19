from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'birthdate')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined')
    readonly_fields = ('last_login', 'date_joined', )
    ordering = ('email', )
    list_filter = ('is_staff', )
    search_fields = ('email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
