import django_filters

from cobranca.models import (
    TipoCobranca,
    PosicaoCheque,
    Alinea,
    Banco,
    Lugar,
    PosicaoContrato,
    Andamento,
    Escritorio,
    Entidade, Responsavel,
)


class BaseNomeFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome",
        lookup_expr="icontains",
        required=False,
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


class PosicaoChequeFilter(BaseNomeFilter):
    class Meta:
        model = PosicaoCheque
        fields = ["nome"]


class LugarFilter(BaseNomeFilter):
    class Meta:
        model = Lugar
        fields = ["nome"]


class EntidadeFilter(BaseNomeFilter):
    class Meta:
        model = Entidade
        fields = ["nome"]


class PosicaoContratoFilter(BaseNomeFilter):
    class Meta:
        model = PosicaoContrato
        fields = ["nome"]


class AndamentoFilter(BaseNomeFilter):
    class Meta:
        model = Andamento
        fields = ["nome"]

class ResponsavelFilter(BaseNomeFilter):
    entidade = django_filters.CharFilter(
        field_name="entidade_id",
        required=False,
    )

    class Meta:
        model = Responsavel
        fields = ["nome", "entidade"]


class EscolaFilter(BaseNomeFilter):
    entidade = django_filters.CharFilter(
        field_name="entidade_id",
        required=False,
    )


class DividaFilter(django_filters.FilterSet):
    codigo_aluno = django_filters.CharFilter(
        field_name="codigoAluno",
        required=False,
    )
    ano = django_filters.CharFilter(
        field_name="ano",
        required=False,
    )
    entidade = django_filters.CharFilter(
        field_name="entidade_id",
        required=False,
    )
