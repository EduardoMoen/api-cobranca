import django_filters

from cobranca.models import TipoCobranca, PosicaoCheque, Alinea, Banco, Lugar, PosicaoContrato, Andamento, Escritorio


class BaseNomeFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome",
        lookup_expr="icontains",
        required=False,
    )

    class Meta:
        abstract = True


class BaseNomeEscritorioFilter(BaseNomeFilter):
    escritorio = django_filters.UUIDFilter(
        field_name="escritorio_id",
        required=True,
    )

    class Meta:
        abstract = True


class TipoCobrancaFilter(BaseNomeFilter):
    class Meta:
        model = TipoCobranca
        fields = ["nome"]


class AlineaFilter(BaseNomeFilter):
    class Meta:
        model = Alinea
        fields = ["nome"]


class BancoFilter(BaseNomeFilter):
    class Meta:
        model = Banco
        fields = ["nome"]


class EscritorioFilter(BaseNomeFilter):
    class Meta:
        model = Escritorio
        fields = ["nome"]


class PosicaoChequeFilter(BaseNomeEscritorioFilter):
    class Meta:
        model = PosicaoCheque
        fields = ["nome", "escritorio"]


class LugarFilter(BaseNomeEscritorioFilter):
    class Meta:
        model = Lugar
        fields = ["nome", "escritorio"]


class PosicaoContratoFilter(BaseNomeEscritorioFilter):
    class Meta:
        model = PosicaoContrato
        fields = ["nome", "escritorio"]


class AndamentoFilter(BaseNomeEscritorioFilter):
    class Meta:
        model = Andamento
        fields = ["nome", "escritorio"]
