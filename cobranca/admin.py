from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cobranca.models import Usuario, Escritorio, Responsavel, Entidade, Escola


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

@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "entidade")

@admin.register(Entidade)
class EntidadeAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "escritorio")


@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ("id", "codigo", "nome", "entidade")
