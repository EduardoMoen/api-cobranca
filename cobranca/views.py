from rest_framework import status
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
    BoletoSerializer,
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
    queryset = PosicaoCheque.objects.all()
    serializer_class = PosicaoChequeSerializer

    def get_filterset_class(self):
        if self.request.method == 'GET':
            return PosicaoChequeFilter

        return None


class EntidadeViewSet(ModelViewSet):
    queryset = Entidade.objects.all()
    serializer_class = EntidadeSerializer

    def get_filterset_class(self):
        if self.request.method == 'GET':
            return EntidadeFilter

        return None


class EscolaViewSet(ModelViewSet):
    queryset = Escola.objects.all()
    serializer_class = EscolaSerializer


class ResponsavelViewSet(ModelViewSet):
    queryset = Responsavel.objects.all()
    serializer_class = ResponsavelSerializer


class PosicaoContratoViewSet(ModelViewSet):
    queryset = PosicaoContrato.objects.all()
    serializer_class = PosicaoContratoSerializer

    def get_filterset_class(self):
        if self.request.method == 'GET':
            return PosicaoContratoFilter

        return None


class LugarViewSet(ModelViewSet):
    queryset = Lugar.objects.all()
    serializer_class = LugarSerializer

    def get_filterset_class(self):
        if self.request.method == 'GET':
            return LugarFilter

        return None


class AndamentoViewSet(ModelViewSet):
    queryset = Andamento.objects.all()
    serializer_class = AndamentoSerializer

    def get_filterset_class(self):
        if self.request.method == 'GET':
            return AndamentoFilter

        return None


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
