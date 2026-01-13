import django_filters

from cobranca.models import TipoCobranca


class TipoCobrancaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome",
        lookup_expr="icontains",
    )

    class Meta:
        model = TipoCobranca
        fields = ["nome"]
