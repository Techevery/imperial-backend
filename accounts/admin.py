from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Manager, LandLord, Tenant
from .forms import CustomUserForm, CustomUserChangeForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserForm
    form = CustomUserChangeForm
    ordering = ('email',)
    list_display = ['email', 'is_staff', 'is_superuser']
    search_fields = ('email',)
    fieldsets = (
        (
            'Fields',
            {
                'fields': (
                    'email',
                    'date_joined',
                    'last_login',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                    'password',
                )
            },
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),

        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(LandLord)
admin.site.register(Manager)
