from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cobranca.models import Usuario, Escritorio, Responsavel, Entidade, Escola, Divida, Boleto, ResponsavelImportacao, \
    BoletoImportacao, TelefoneImportacao


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


@admin.register(Divida)
class DividaAdmin(admin.ModelAdmin):
    list_display = ("id", "numeroCobranca", "entidade")

admin.site.register(Boleto)

@admin.register(ResponsavelImportacao)
class ResponsavelImportacaoAdmin(admin.ModelAdmin):
    list_display = ["nome","cpf", "rg"]

@admin.register(BoletoImportacao)
class BoletoImportacaoAdmin(admin.ModelAdmin):
    list_display = ["codigo_carne", "valor", "responsavel"]

@admin.register(TelefoneImportacao)
class TelefoneImportacaoAdmin(admin.ModelAdmin):
    list_display = ["responsavel", "numero", "descricao"]
