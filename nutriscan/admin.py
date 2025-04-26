from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import AditionalInfoUser

# Crear el Inline
class AditionalInfoUserInline(admin.StackedInline):
    model = AditionalInfoUser
    can_delete = False
    verbose_name_plural = 'Información adicional'
    fk_name = 'user'

# Extender el admin original de User
class CustomUserAdmin(DefaultUserAdmin):
    inlines = (AditionalInfoUserInline,)

# Re-registrar el modelo User con nuestro CustomAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
