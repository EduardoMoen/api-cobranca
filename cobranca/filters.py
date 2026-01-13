import django_filters

from cobranca.models import TipoCobranca, PosicaoCheque


class TipoCobrancaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome",
        lookup_expr="icontains",
    )

    class Meta:
        model = TipoCobranca
        fields = ["nome"]


class PosicaoChequeFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome",
        lookup_expr="icontains",
        required=False,
    )
    escritorio = django_filters.CharFilter(
        field_name="escritorio_id",
        required=True,
    )

    class Meta:
        model = PosicaoCheque
        fields = ["nome", "escritorio"]
