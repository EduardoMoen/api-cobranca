import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class TipoCobranca(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome}"


class Banco(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome}"


class Escritorio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome}"


class PosicaoCheque(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    escritorio = models.ForeignKey(Escritorio, on_delete=models.PROTECT, related_name="posicao_cheques")

    class Meta:
        ordering = ("nome",)

    def __str__(self):
        return f"{self.nome}"


class Entidade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    escritorio = models.ForeignKey(Escritorio, on_delete=models.PROTECT, related_name="entidades")

    def __str__(self):
        return f"{self.nome}"


class Escola(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    cep = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    obs = models.CharField(max_length=255, null=True, blank=True)
    entidade = models.ForeignKey(Entidade, on_delete=models.PROTECT, related_name="escolas")

    def __str__(self):
        return f"{self.nome}"


class Responsavel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    nascimento = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    cep = models.CharField(max_length=255, null=True, blank=True)
    rg = models.CharField(max_length=255, null=True, blank=True)
    rg_emissao = models.DateField(null=True, blank=True)
    estado_civil = models.CharField(max_length=255, null=True, blank=True)
    telefones = models.CharField(max_length=255, null=True, blank=True)
    entidade = models.ForeignKey(Entidade, on_delete=models.PROTECT, related_name="responsaveis")

    def __str__(self):
        return f"{self.nome}"


class PosicaoContrato(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    escritorio = models.ForeignKey(Escritorio, on_delete=models.PROTECT, related_name="posicao_contratos")

    def __str__(self):
        return f"{self.nome}"


class Lugar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    escritorio = models.ForeignKey(Escritorio, on_delete=models.PROTECT, related_name="lugares")

    def __str__(self):
        return f"{self.nome}"


class Andamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    escritorio = models.ForeignKey(Escritorio, on_delete=models.PROTECT, related_name="andamentos")

    def __str__(self):
        return f"{self.nome}"


class Alinea(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome}"


class Acordo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.PROTECT, related_name="acordos")
    data = models.DateField()
    valor = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.responsavel} {self.valor}"


class AcordoParcelas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vencimento = models.DateField()
    valor = models.DecimalField(decimal_places=2, max_digits=10)
    data_pagamento = models.DateField()
    acordo = models.ForeignKey(Acordo, on_delete=models.PROTECT, related_name="acordo_parcelas")

    def __str__(self):
        return f"{self.acordo} {self.vencimento}"


class Boleto(models.Model):
    codigoEscola = models.CharField(max_length=255)
    codigoAluno = models.IntegerField()
    codigoCarne = models.IntegerField()
    numeroCarne = models.CharField(max_length=255)
    dataVencimento = models.DateTimeField()
    valor = models.DecimalField(decimal_places=2, max_digits=10)
    multa = models.DecimalField(decimal_places=2, max_digits=10)
    percentualMulta = models.DecimalField(decimal_places=2, max_digits=10)
    jurosDia = models.DecimalField(decimal_places=2, max_digits=10)
    percentualJuro = models.DecimalField(decimal_places=2, max_digits=10)
    serieTurma = models.CharField(max_length=255)
    statusCobranca = models.IntegerField()

    def __str__(self):
        return f"{self.codigoEscola} {self.codigoAluno}"


class Usuario(AbstractUser):
    escritorio = models.ForeignKey(
        Escritorio,
        on_delete=models.PROTECT,
        related_name="usuarios",
        null=True,
        blank=True,
    )
