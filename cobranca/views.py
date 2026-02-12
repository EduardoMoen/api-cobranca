from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from cobranca.filters import (
    TipoCobrancaFilter,
    AlineaFilter,
    BancoFilter,
    EscritorioFilter,
    PosicaoChequeFilter,
    LugarFilter,
    PosicaoContratoFilter,
    AndamentoFilter,
    EntidadeFilter, ResponsavelFilter, EscolaFilter, DividaFilter,
)
from cobranca.models import (
    TipoCobranca,
    Banco,
    Escritorio,
    PosicaoCheque,
    Entidade,
    Escola,
    Responsavel,
    PosicaoContrato,
    Alinea,
    Boleto,
    Lugar,
    Andamento,
    Acordo,
    AcordoParcelas, Divida,
)
from .pdf.extrato import gerar_extrato_pdf
from cobranca.serializers import (
    TipoCobrancaSerializer,
    BancoSerializer,
    EscritorioSerializer,
    PosicaoChequeSerializer,
    EntidadeSerializer,
    EscolaSerializer,
    ResponsavelSerializer,
    PosicaoContratoSerializer,
    LugarSerializer,
    AndamentoSerializer,
    AlineaSerializer,
    AcordoSerializer,
    AcordoParcelasSerializer,
    BoletoSerializer, DividaSerializer, ResponsavelListSerializer, EscolaListSerializer, DividaListSerializer,
)
from cobranca.services import get_external_data


class TipoCobrancaViewSet(ModelViewSet):
    queryset = TipoCobranca.objects.all()
    serializer_class = TipoCobrancaSerializer
    filterset_class = TipoCobrancaFilter


class BancoViewSet(ModelViewSet):
    queryset = Banco.objects.all()
    serializer_class = BancoSerializer
    filterset_class = BancoFilter


class EscritorioViewSet(ModelViewSet):
    queryset = Escritorio.objects.all()
    serializer_class = EscritorioSerializer
    filterset_class = EscritorioFilter


class PosicaoChequeViewSet(ModelViewSet):
    serializer_class = PosicaoChequeSerializer
    filterset_class = PosicaoChequeFilter

    def get_queryset(self):
        queryset = PosicaoCheque.objects.all()

        if self.request.method == 'GET':
            user = self.request.user
            queryset = queryset.filter(escritorio_id=user.escritorio_id)

        return queryset


class EntidadeViewSet(ModelViewSet):
    serializer_class = EntidadeSerializer
    filterset_class = EntidadeFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Entidade.objects.filter(escritorio_id=user.escritorio_id)

        return queryset


class EscolaViewSet(ModelViewSet):
    serializer_class = EscolaSerializer
    filterset_class = EscolaFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Escola.objects.select_related(
            "entidade", "entidade__escritorio"
        ).filter(entidade__escritorio_id=user.escritorio_id)

        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return EscolaListSerializer

        return EscolaSerializer


class ResponsavelViewSet(ModelViewSet):
    serializer_class = ResponsavelSerializer
    filterset_class = ResponsavelFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Responsavel.objects.select_related(
            "entidade", "entidade__escritorio"
        ).filter(entidade__escritorio_id=user.escritorio_id)

        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ResponsavelListSerializer

        return ResponsavelSerializer


class PosicaoContratoViewSet(ModelViewSet):
    serializer_class = PosicaoContratoSerializer
    filterset_class = PosicaoContratoFilter

    def get_queryset(self):
        user = self.request.user
        queryset = PosicaoContrato.objects.filter(escritorio_id=user.escritorio_id)

        return queryset


class LugarViewSet(ModelViewSet):
    serializer_class = LugarSerializer
    filterset_class = LugarFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Lugar.objects.filter(escritorio_id=user.escritorio_id)

        return queryset


class AndamentoViewSet(ModelViewSet):
    serializer_class = AndamentoSerializer
    filterset_class = AndamentoFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Andamento.objects.filter(escritorio_id=user.escritorio_id)

        return queryset


class AlineaViewSet(ModelViewSet):
    queryset = Alinea.objects.all()
    serializer_class = AlineaSerializer
    filterset_class = AlineaFilter


class AcordoViewSet(ModelViewSet):
    queryset = Acordo.objects.all()
    serializer_class = AcordoSerializer


class AcordoParcelasViewSet(ModelViewSet):
    queryset = AcordoParcelas.objects.all()
    serializer_class = AcordoParcelasSerializer


class BoletoViewSet(ModelViewSet):
    queryset = Boleto.objects.all()
    serializer_class = BoletoSerializer


class DividaViewSet(ModelViewSet):
    serializer_class = DividaSerializer
    filterset_class = DividaFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Divida.objects.select_related(
            "entidade",
            "responsavel",
            "responsavelAtual",
            "escola",
            "posicaoContrato",
            "posicaoCheque",
            "andamento",
            "lugar",
            "acordo",
        ).filter(entidade__escritorio_id=user.escritorio_id)

        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return DividaListSerializer

        return DividaSerializer


class ImportBoletosView(APIView):
    def post(self, request):
        data = get_external_data()
        if not data or "result" not in data:
            return Response({"error": "Não foi possível obter dados da API"}, status=status.HTTP_400_BAD_REQUEST)

        items = data["result"]
        serializer = BoletoSerializer(data=items, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def extrato_view(request, responsavel_id):
    #Busca responsavel
    responsavel = get_object_or_404(Responsavel, id=responsavel_id)

    dividas = responsavel.dividas.all().order_by("dataVencimento")

    pdf_buffer = gerar_extrato_pdf(responsavel, dividas)

    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="extrato_{responsavel.nome}.pdf"'
    )

    return response
