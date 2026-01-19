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
    Boleto,
)


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
    class Meta:
        model = Escola
        fields = "__all__"


class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = "__all__"


class ResponsavelListSerializer(ResponsavelSerializer):
    entidade_nome = serializers.CharField(
        source="entidade.nome",
        read_only=True,
    )


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
