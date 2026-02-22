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


class Divida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # -------- Coluna 1 --------
    entidade = models.ForeignKey(Entidade, on_delete=models.PROTECT, related_name="dividas")
    responsavel = models.ForeignKey(Responsavel, on_delete=models.PROTECT, related_name="dividas")
    tipoCobranca = models.ForeignKey(TipoCobranca, on_delete=models.PROTECT, related_name="dividas")
    numeroCobranca = models.CharField(max_length=20)
    dataPrimeiraImportacao = models.DateField(null=True, blank=True)
    dataUltimaImportacao = models.DateField(null=True, blank=True)
    banco = models.ForeignKey(Banco, null=True, blank=True, on_delete=models.PROTECT, related_name="dividas")
    agencia = models.CharField(max_length=10, null=True, blank=True)
    conta = models.CharField(max_length=50, null=True, blank=True,)
    alinea = models.ForeignKey(Alinea, null=True, blank=True, on_delete=models.PROTECT, related_name="dividas")
    dataVencimento = models.DateField()
    valorCobranca = models.DecimalField(decimal_places=2, max_digits=10)
    valorCobrancaAcao = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    statusValorAcao = models.BooleanField(null=True, blank=True)
    parcela = models.CharField(max_length=50, null=True, blank=True)
    valorMulta = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    valorJuro = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    dataAcertoMantenedora = models.DateField(null=True, blank=True)
    valorPago = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    numeroContrato = models.CharField(max_length=50, null=True, blank=True)
    responsavelAtual = models.ForeignKey(Responsavel, null=True, blank=True, on_delete=models.PROTECT, related_name="atual_dividas")
    statusBolsista = models.BooleanField(null=True, blank=True)
    statusEstornado = models.BooleanField(null=True, blank=True)
    codigoAluno = models.IntegerField(null=True, blank=True)
    nomeAluno = models.CharField(max_length=50, null=True, blank=True)
    serie = models.CharField(max_length=50, null=True, blank=True)
    escola = models.ForeignKey(Escola, null=True, blank=True, on_delete=models.PROTECT, related_name="dividas")
    ano = models.IntegerField(null=True, blank=True)
    # -------- Coluna 2 --------
    dataInicioJuro = models.DateField(null=True, blank=True)
    dataAcertoJw = models.DateField(null=True, blank=True)
    numeroDias = models.IntegerField(null=True, blank=True)
    mesInicioCorrecao = models.IntegerField(null=True, blank=True)
    anoInicioCorrecao = models.IntegerField(null=True, blank=True)
    indiceInicial = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    mesFimCorrecao = models.IntegerField(null=True, blank=True)
    anoFimCorrecao = models.IntegerField(null=True, blank=True)
    indiceFinal = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    valorCorrigido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentualMulta = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    valorMultaJw = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentualJuros = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    valorJuroJw = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valorSubtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentualHonorarios = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    valorHonorarios = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    statusPagoJw = models.BooleanField(null=True, blank=True)
    dataPagoJw = models.DateField(null=True, blank=True)
    valorCobrado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # ---------- Coluna 3 ----------
    numeroRecibo = models.IntegerField(null=True, blank=True)
    dataImpressaoCarta = models.DateField(null=True, blank=True)
    nomeResponsavelCobranca = models.CharField(max_length=50, null=True, blank=True)
    posicaoContrato = models.ForeignKey(PosicaoContrato, null=True, blank=True, on_delete=models.PROTECT, related_name="dividas")
    posicaoCheque = models.ForeignKey(PosicaoCheque, null=True, blank=True, on_delete=models.PROTECT, related_name="dividas")
    andamento = models.ForeignKey(Andamento, null=True, blank=True, on_delete=models.PROTECT, related_name="dividas")
    lugar = models.ForeignKey(Lugar, null=True, blank=True, on_delete=models.PROTECT, related_name="dividas")
    statusAcao = models.BooleanField(null=True, blank=True)
    statusSpcNaoEnviar = models.BooleanField(null=True, blank=True)
    pasta = models.CharField(max_length=255, null=True, blank=True)
    numeroVara = models.CharField(max_length=255, null=True, blank=True)
    numeroProcesso = models.CharField(max_length=255, null=True, blank=True)
    dataAcao = models.DateField(null=True, blank=True)
    # ---------- Coluna 4 ----------
    statusNaoEnviarCarta = models.BooleanField(null=True, blank=True)
    statusAcordo = models.BooleanField(null=True, blank=True)
    dataResponsavelCobranca = models.DateField(null=True, blank=True)
    dataSpcEnvio = models.DateField(null=True, blank=True)
    statusSpcEnvio = models.TextField(null=True, blank=True)
    dataSpcBaixa = models.DateField(null=True, blank=True)
    statusSpcBaixa = models.TextField(null=True, blank=True)
    statusSpcBaixaManual = models.BooleanField(null=True, blank=True)
    statusSpcBaixar = models.BooleanField(null=True, blank=True)
    remessaSpcEnvio = models.IntegerField(null=True, blank=True)
    remessaSpcBaixa = models.IntegerField(null=True, blank=True)
    dataAcertoJwMantenedora = models.DateField(null=True, blank=True)
    obsJw = models.TextField(null=True, blank=True)
    acordo = models.ForeignKey(Acordo, null=True, blank=True, on_delete=models.PROTECT, related_name="dividas")

    def __str__(self):
        return f"{self.numeroCobranca}"


class Indice(models.Model):
    ano = models.IntegerField()
    mes = models.IntegerField()
    indice = models.DecimalField(max_digits=16, decimal_places=8)

    def __str__(self):
        return f"{self.indice}"


class ResponsavelImportacao(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    codigo_escola = models.CharField(max_length=50)
    cpf = models.CharField(max_length=20)
    nome = models.CharField(max_length=255)
    rg = models.CharField(max_length=50, null=True, blank=True)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=20)
    email = models.EmailField()
    nacionalidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class BoletoImportacao(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    responsavel = models.ForeignKey(
        ResponsavelImportacao,
        on_delete=models.PROTECT,
        related_name="boletos",
    )

    codigo_carne = models.BigIntegerField()
    codigo_aluno = models.BigIntegerField()
    numero_carne = models.CharField(max_length=100)
    data_vencimento = models.DateTimeField()

    valor = models.DecimalField(max_digits=12, decimal_places=2)
    multa = models.DecimalField(max_digits=12, decimal_places=2)
    percentual_multa = models.DecimalField(max_digits=5, decimal_places=2)
    juros_dia = models.DecimalField(max_digits=10, decimal_places=4)
    percentual_juro = models.DecimalField(max_digits=5, decimal_places=2)

    serie_turma = models.CharField(max_length=100)
    status_cobranca = models.IntegerField()
    aluno_nome = models.CharField(max_length=255)
    aluno_genero = models.CharField(max_length=1)
    aluno_data_nascimento = models.DateTimeField()

    def __str__(self):
        return f"{self.numero_carne} - {self.aluno_nome}"


class TelefoneImportacao(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    responsavel = models.ForeignKey(
        ResponsavelImportacao,
        on_delete=models.PROTECT,
        related_name="telefones",
    )

    numero = models.CharField(max_length=30)
    descricao = models.CharField(max_length=255, blank=True)
    e_principal = models.BooleanField(default=False)

    def __str__(self):
        return self.numero
