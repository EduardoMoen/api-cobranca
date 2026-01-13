from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cobranca.models import Usuario, Escritorio

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    pass

admin.site.register(Escritorio)