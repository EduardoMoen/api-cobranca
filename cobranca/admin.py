from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cobranca.models import Usuario, Escritorio

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Escritório", {"fields": ("escritorio",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Escritório", {"fields": ("escritorio",)}),
    )

@admin.register(Escritorio)
class EscritorioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
