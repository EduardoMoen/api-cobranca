from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
    EntidadeFilter,
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
    AcordoParcelas,
)
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
    BoletoSerializer, ResponsavelListSerializer,
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
        queryset = Entidade.objects.all()

        if self.request.method == 'GET':
            user = self.request.user
            queryset = queryset.filter(escritorio_id=user.escritorio_id)

        return queryset


class EscolaViewSet(ModelViewSet):
    queryset = Escola.objects.all()
    serializer_class = EscolaSerializer


class ResponsavelViewSet(ModelViewSet):
    queryset = Responsavel.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.select_related()

        return queryset


    def get_serializer_class(self):
        if self.action == "list":
            return ResponsavelListSerializer

        return ResponsavelSerializer


class PosicaoContratoViewSet(ModelViewSet):
    serializer_class = PosicaoContratoSerializer
    filterset_class = PosicaoContratoFilter

    def get_queryset(self):
        queryset = PosicaoContrato.objects.all()

        if self.request.method == 'GET':
            user = self.request.user
            queryset = queryset.filter(escritorio_id=user.escritorio_id)

        return queryset


class LugarViewSet(ModelViewSet):
    serializer_class = LugarSerializer
    filterset_class = LugarFilter

    def get_queryset(self):
        queryset = Lugar.objects.all()

        if self.request.method == 'GET':
            user = self.request.user
            queryset = queryset.filter(escritorio_id=user.escritorio_id)

        return queryset


class AndamentoViewSet(ModelViewSet):
    serializer_class = AndamentoSerializer
    filterset_class = AndamentoFilter

    def get_queryset(self):
        queryset = Andamento.objects.all()

        if self.request.method == 'GET':
            user = self.request.user
            queryset = queryset.filter(escritorio_id=user.escritorio_id)

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
