from rest_framework import serializers
from cobranca.models import (
    TipoCobranca,
    Banco,
    Escritorio,
    PosicaoCheque,
    Entidade,
    Escola,
    Responsavel,
    PosicaoContrato,
    Lugar,
    Andamento,
    Alinea,
    Acordo,
    AcordoParcelas,
    Boleto, Divida, TelefoneImportacao, BoletoImportacao, ResponsavelImportacao, Indice,
)


class NestedPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        # Se vier objeto {"id": "..."}
        if isinstance(data, dict):
            data = data.get("id")

        return super().to_internal_value(data)


class TipoCobrancaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCobranca
        fields = "__all__"


class BancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banco
        fields = "__all__"


class EscritorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escritorio
        fields = "__all__"


class PosicaoChequeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosicaoCheque
        fields = "__all__"


class EntidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidade
        fields = "__all__"


class EscolaSerializer(serializers.ModelSerializer):
    entidade = NestedPrimaryKeyRelatedField(
        queryset=Entidade.objects.all()
    )

    class Meta:
        model = Escola
        fields = "__all__"


class EscolaListSerializer(EscolaSerializer):
    entidade = EntidadeSerializer(read_only=True)


class ResponsavelSerializer(serializers.ModelSerializer):
    entidade = NestedPrimaryKeyRelatedField(
        queryset=Entidade.objects.all()
    )

    class Meta:
        model = Responsavel
        fields = "__all__"


class ResponsavelListSerializer(ResponsavelSerializer):
    entidade = EntidadeSerializer(read_only=True)


class PosicaoContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosicaoContrato
        fields = "__all__"


class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = "__all__"


class AndamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Andamento
        fields = "__all__"


class AlineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alinea
        fields = "__all__"


class AcordoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acordo
        fields = "__all__"


class AcordoParcelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcordoParcelas
        fields = "__all__"


class BoletoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleto
        fields = "__all__"


class DividaSerializer(serializers.ModelSerializer):
    entidade = NestedPrimaryKeyRelatedField(
        queryset=Entidade.objects.all()
    )
    responsavel = NestedPrimaryKeyRelatedField(
        queryset=Responsavel.objects.all()
    )
    responsavelAtual = NestedPrimaryKeyRelatedField(
        queryset=Responsavel.objects.all(),
        required = False,
        allow_null = True,
    )
    escola = NestedPrimaryKeyRelatedField(
        queryset=Escola.objects.all(),
        required=False,
        allow_null=True,
    )
    posicaoContrato = NestedPrimaryKeyRelatedField(
        queryset=PosicaoContrato.objects.all(),
        required=False,
        allow_null=True,
    )
    posicaoCheque = NestedPrimaryKeyRelatedField(
        queryset=PosicaoCheque.objects.all(),
        required=False,
        allow_null=True,
    )
    andamento = NestedPrimaryKeyRelatedField(
        queryset=Andamento.objects.all(),
        required=False,
        allow_null=True,
    )
    lugar = NestedPrimaryKeyRelatedField(
        queryset=Lugar.objects.all(),
        required=False,
        allow_null=True,
    )
    acordo = NestedPrimaryKeyRelatedField(
        queryset=Acordo.objects.all(),
        required=False,
        allow_null=True,
    )
    banco = NestedPrimaryKeyRelatedField(
        queryset=Banco.objects.all(),
        required=False,
        allow_null=True,
    )
    alinea = NestedPrimaryKeyRelatedField(
        queryset=Alinea.objects.all(),
        required=False,
        allow_null=True,
    )
    tipoCobranca = NestedPrimaryKeyRelatedField(
        queryset=TipoCobranca.objects.all()
    )

    class Meta:
        model = Divida
        fields = "__all__"


class DividaListSerializer(DividaSerializer):
    entidade = EntidadeSerializer(read_only=True)
    responsavel = ResponsavelSerializer(read_only=True)
    responsavelAtual = ResponsavelSerializer(read_only=True)
    escola = EscolaSerializer(read_only=True)
    posicaoContrato = PosicaoContratoSerializer(read_only=True)
    posicaoCheque = PosicaoChequeSerializer(read_only=True)
    andamento = AndamentoSerializer(read_only=True)
    lugar = LugarSerializer(read_only=True)
    acordo = AcordoSerializer(read_only=True)
    banco = BancoSerializer(read_only=True)
    alinea = AlineaSerializer(read_only=True)
    tipoCobranca = TipoCobrancaSerializer(read_only=True)


class TelefoneImportacaoSerializer(serializers.ModelSerializer):
    ePrincipal = serializers.BooleanField(source="e_principal")

    class Meta:
        model = TelefoneImportacao
        fields = [
            "numero",
            "descricao",
            "ePrincipal",
        ]


class BoletoImportacaoSerializer(serializers.ModelSerializer):
    codigoCarne = serializers.IntegerField(source="codigo_carne")
    codigoAluno = serializers.IntegerField(source="codigo_aluno")
    numeroCarne = serializers.CharField(source="numero_carne")
    dataVencimento = serializers.DateTimeField(source="data_vencimento")

    percentualMulta = serializers.DecimalField(
        max_digits=5, decimal_places=2, source="percentual_multa"
    )
    jurosDia = serializers.DecimalField(
        max_digits=10, decimal_places=4, source="juros_dia"
    )
    percentualJuro = serializers.DecimalField(
        max_digits=5, decimal_places=2, source="percentual_juro"
    )

    serieTurma = serializers.CharField(source="serie_turma")
    statusCobranca = serializers.IntegerField(source="status_cobranca")
    alunoNome = serializers.CharField(source="aluno_nome")
    alunoGenero = serializers.CharField(source="aluno_genero")
    alunoDataNascimento = serializers.DateTimeField(source="aluno_data_nascimento")

    class Meta:
        model = BoletoImportacao
        fields = [
            "codigoCarne",
            "codigoAluno",
            "numeroCarne",
            "dataVencimento",
            "valor",
            "multa",
            "percentualMulta",
            "jurosDia",
            "percentualJuro",
            "serieTurma",
            "statusCobranca",
            "alunoNome",
            "alunoGenero",
            "alunoDataNascimento",
        ]


class ResponsavelImportacaoSerializer(serializers.ModelSerializer):
    codigoEscola = serializers.CharField(source="codigo_escola")
    barrio = serializers.CharField(source="bairro")

    boletos = BoletoImportacaoSerializer(many=True)
    telefones = TelefoneImportacaoSerializer(many=True)

    class Meta:
        model = ResponsavelImportacao
        fields = [
            "codigoEscola",
            "cpf",
            "nome",
            "rg",
            "endereco",
            "barrio",
            "cidade",
            "uf",
            "cep",
            "email",
            "nacionalidade",
            "boletos",
            "telefones",
        ]

    def create(self, validated_data):
        boletos_data = validated_data.pop("boletos", [])
        telefones_data = validated_data.pop("telefones", [])

        responsavel = ResponsavelImportacao.objects.create(**validated_data)

        for boleto in boletos_data:
            BoletoImportacao.objects.create(responsavel=responsavel, **boleto)

        for telefone in telefones_data:
            TelefoneImportacao.objects.create(responsavel=responsavel, **telefone)

        return responsavel


class IndiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indice
        fields = "__all__"
