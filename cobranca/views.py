import datetime
import csv
import io
import re

from decimal import Decimal

from django.utils import timezone
from django.db import transaction
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

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
    BoletoApi,
    Lugar,
    Andamento,
    Acordo,
    AcordoParcelas, Divida, ResponsavelImportacao, Indice, BoletoImportacao,
)
from .pdf.carta import gerar_carta_pdf
from .pdf.carta_por_entidade import carta_por_entidade
from .pdf.carta_word import gerar_carta_word
from .pdf.cartas_entidade_word import gerar_carta_entidade_word
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
    ResponsavelImportacaoSerializer, IndiceSerializer, ResponsavelApiSerializer,
)
from cobranca.services import get_external_data, importar_responsaveis_com_boletos, get_responsaveis_api, enviar_email


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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        instance = self.get_queryset().get(pk=response.data["id"])
        serializer = EscolaListSerializer(instance, context={"request": request})

        return Response(serializer.data, status=response.status_code)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        instance = self.get_queryset().get(pk=response.data["id"])
        serializer = EscolaListSerializer(instance, context={"request": request})

        return Response(serializer.data, status=response.status_code)


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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        instance = self.get_queryset().get(pk=response.data["id"])
        serializer = ResponsavelListSerializer(instance, context={"request": request})

        return Response(serializer.data, status=response.status_code)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        instance = self.get_queryset().get(pk=response.data["id"])
        serializer = ResponsavelListSerializer(instance, context={"request": request})

        return Response(serializer.data, status=response.status_code)


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


class IndiceViewSet(ModelViewSet):
    queryset = Indice.objects.all()
    serializer_class = IndiceSerializer


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
            "banco",
            "alinea",
            "tipoCobranca",
        ).filter(entidade__escritorio_id=user.escritorio_id)

        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return DividaListSerializer

        return DividaSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        instance = self.get_queryset().get(pk=response.data["id"])
        serializer = DividaListSerializer(instance, context={"request": request})

        return Response(serializer.data, status=response.status_code)

    def perform_update(self, serializer):
        serializer.save(
            alterado_por=self.request.user,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        instance = self.get_queryset().get(pk=response.data["id"])
        serializer = DividaListSerializer(instance, context={"request": request})

        return Response(serializer.data, status=response.status_code)

    def _buscar_indice(self, indices, ano, mes):
        valor = 0
        for indice in indices:
            if (indice.ano < ano) or (indice.ano == ano and indice.mes <= mes):
                valor = indice.indice
            else:
                break

        return valor

    @action(
        detail=True,
        methods=["post"],
        url_path=r"calculado/(?P<honorarios>\d+)"
    )
    def calculado(self, request, pk=None, honorarios=None):
        valor_multa = Decimal(2)
        valor_juros = Decimal(1)
        valor_honorarios = Decimal(honorarios)

        dividas = Divida.objects.filter(responsavel_id=pk)

        indices = list(
            Indice.objects.all().order_by("ano", "mes")
        )

        for divida in dividas:
            divida.dataInicioJuro = divida.dataVencimento
            divida.dataAcertoJw = datetime.date.today()

            divida.numeroDias = (
                divida.dataAcertoJw - divida.dataInicioJuro
            ).days

            divida.mesInicioCorrecao = divida.dataInicioJuro.month
            divida.anoInicioCorrecao = divida.dataInicioJuro.year
            divida.indiceInicial = self._buscar_indice(
                indices,
                divida.anoInicioCorrecao,
                divida.mesInicioCorrecao,
            )

            divida.mesFimCorrecao = divida.dataAcertoJw.month
            divida.anoFimCorrecao = divida.dataAcertoJw.year
            divida.indiceFinal = self._buscar_indice(
                indices,
                divida.anoFimCorrecao,
                divida.mesFimCorrecao,
            )

            divida.valorCorrigido = divida.valorCobranca / divida.indiceInicial * divida.indiceFinal

            divida.percentualMulta = valor_multa
            divida.valorMultaJw = divida.percentualMulta * divida.valorCobranca / 100

            divida.percentualJuros = valor_juros
            divida.valorJuroJw = divida.valorCorrigido * divida.numeroDias * divida.percentualJuros / 100 / 30

            divida.valorSubtotal = divida.valorCorrigido + divida.valorMultaJw + divida.valorJuroJw

            divida.percentualHonorarios = valor_honorarios
            divida.valorHonorarios = divida.valorSubtotal * divida.percentualHonorarios / 100

            divida.valorTotal = divida.valorSubtotal + divida.valorHonorarios

            divida.save()

        serializer = DividaListSerializer(dividas, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def zerado(self, request, pk=None):

        dividas = Divida.objects.filter(responsavel_id=pk)

        dividas.update(percentualJuros=Decimal("0"))

        serializer = DividaListSerializer(dividas, many=True)

        return Response(serializer.data)


class ImportBoletosView(APIView):
    def post(self, request):
        data = get_external_data(page_size=1000)

        if not data or "result" not in data:
            return Response({"error": "Não foi possível obter dados da API"}, status=status.HTTP_400_BAD_REQUEST)

        items = data["result"]
        serializer = BoletoSerializer(data=items, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImportResponsaveisApi(APIView):
    def post(self, request):
        data = get_responsaveis_api(page_size=1000)

        if not data or "result" not in data:
            return Response({"error": "Não foi possível obter dados da API"}, status=status.HTTP_400_BAD_REQUEST)

        items = data["result"]
        serializer = ResponsavelApiSerializer(data=items, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImportarResponsaveisComBoletos(APIView):
    def post(self, request):
        data = importar_responsaveis_com_boletos(page_size=500)

        if not data or "result" not in data:
            return Response(
                {"error": "Não foi possível obter dados da API"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        items = data["result"]

        erros = []
        total_importados = 0

        for i, item in enumerate(items, start=1):

            serializer = ResponsavelImportacaoSerializer(data=item)

            if serializer.is_valid():
                serializer.save()
                total_importados += 1
            else:
                erros.append({
                    "linha": i,
                    "erros": serializer.errors,
                    "dados": item,
                })

        return Response(
            {
                "total_recebidos": len(items),
                "total_importados": total_importados,
                "total_erros": len(erros),
                "erros": erros,
            },
            status=status.HTTP_200_OK
        )

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


def carta_view(request, responsavel_id):
    responsavel = get_object_or_404(Responsavel, id=responsavel_id)
    dividas = responsavel.dividas.all().order_by("nomeAluno")

    pdf_buffer = gerar_carta_pdf(responsavel, dividas)

    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="carta.pdf"'

    return response

def carta_word_view(request, responsavel_id):
    responsavel = get_object_or_404(Responsavel, id=responsavel_id)
    dividas = responsavel.dividas.all().order_by("nomeAluno")

    word_buffer = gerar_carta_word(responsavel, dividas)

    response = HttpResponse(
        word_buffer,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    response["Content-Disposition"] = (
        'attachment; filename="carta.docx"'
    )

    return response


def carta_por_entidade_view(request, entidade_id):
    entidade = get_object_or_404(Entidade, id=entidade_id)
    dividas = entidade.dividas.all().order_by("responsavel")

    pdf_buffer = carta_por_entidade(dividas)

    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="Carta_entidade.pdf"'

    return response

def carta_por_entidade_word_view(request, entidade_id):
    entidade = get_object_or_404(Entidade, id=entidade_id)
    dividas = entidade.dividas.all().order_by("responsavel")

    word_buffer = gerar_carta_entidade_word(dividas)

    response = HttpResponse(
        word_buffer,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    response["Content-Disposition"] = (
        'attachment; filename="carta.docx"'
    )

    return response

def carta_por_escola_word_view(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    dividas = escola.dividas.all().order_by("responsavel")

    word_buffer = gerar_carta_entidade_word(dividas)

    response = HttpResponse(
        word_buffer,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    response["Content-Disposition"] = (
        'attachment; filename="carta.docx"'
    )

    return response

def carta_por_escola_view(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)
    dividas = escola.dividas.all().order_by("responsavel")

    pdf_buffer = carta_por_entidade(dividas)

    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="Carta_escola.pdf"'

    return response

class EnviarEmail(APIView):
    def post(self, request):

        enviar_email()

        return Response({"message": "Email enviado!"})


class ValidarResponsaveis(APIView):
    def post(self, request):

        importados = ResponsavelImportacao.objects.all()

        criados = 0
        atualizados = 0
        erros = 0

        for item in importados.iterator():

            if not item.cpf:
                continue

            try:
                entidade = Entidade.objects.get(codigo=item.codigo_escola[:6])

                obj, created = Responsavel.objects.update_or_create(
                    cpf=item.cpf,
                    entidade=entidade,
                    defaults={
                        "nome": item.nome,
                        "endereco": item.endereco,
                        "bairro": item.bairro,
                        "cidade": item.cidade,
                        "uf": item.uf,
                        "cep": item.cep,
                        "rg": item.rg,
                        "email": item.email,
                    }
                )

                if created:
                    criados += 1
                else:
                    atualizados += 1

            except Exception as e:
                erros += 1
                print(f"Erro no CPF {item.cpf}: {e}")

        return Response({
            "criados": criados,
            "atualizados": atualizados,
        })


# class ValidarBoletos(APIView):
#     def post(self, request):
#
#         importados = BoletoImportacao.objects.all()
#
#         criados = 0
#         atualizados = 0
#         erros = 0
#
#         tipoCobranca = TipoCobranca.objects.get(id=1)
#
#         entidades = {e.codigo: e for e in Entidade.objects.all()}
#         responsaveis = {r.cpf: r for r in Responsavel.objects.all()}
#
#         for item in importados:
#
#             if not item.numero_carne:
#                 continue
#
#             try:
#                 entidade_codigo = item.responsavel.codigo_escola[:6]
#
#                 entidade = entidades.get(entidade_codigo)
#                 if not entidade:
#                     raise Exception(f"Entidade não encontrada: {entidade}")
#
#                 responsavel = responsaveis.get(item.responsavel.cpf)
#
#                 obj, created = Divida.objects.update_or_create(
#                     codigoCobranca=item.codigo_carne,
#                     defaults={
#                         "numeroCobranca": item.numero_carne,
#                         "responsavel": responsavel,
#                         "tipoCobranca": tipoCobranca,
#                         "dataVencimento": item.data_vencimento,
#                         "valorCobranca": item.valor,
#                         "valorMulta": item.multa,
#                         "codigoAluno": item.codigo_aluno,
#                         "percentualMulta": item.percentual_multa,
#                         "percentualJuros": item.percentual_juro,
#                         "serie": item.serie_turma,
#                         "nomeAluno": item.aluno_nome,
#                         "entidade": entidade,
#                         "escola": item.escola,
#                     }
#                 )
#
#                 if created:
#                     criados += 1
#                 else:
#                     atualizados += 1
#
#             except Exception as e:
#                 erros += 1
#                 print(f"Erro no Codigo {item.codigo_carne}: {e}")
#
#         return Response({
#             "criados": criados,
#             "atualizados": atualizados,
#             "erros": erros
#         })


class ValidarBoletos(APIView):

    def post(self, request):

        importados = (
            BoletoImportacao.objects
            .select_related("responsavel")
            .all()
        )

        criados = 0
        atualizados = 0
        erros = 0

        tipo_cobranca = TipoCobranca.objects.get(id=1)

        entidades = {
            e.codigo: e
            for e in Entidade.objects.all()
        }

        responsaveis = {
            r.cpf: r
            for r in Responsavel.objects.all()
        }

        # carrega tudo uma vez
        dividas = {
            d.codigoCobranca: d
            for d in Divida.objects.all()
        }

        for item in importados:

            if not item.numero_carne:
                continue

            try:

                entidade_codigo = (
                    item.responsavel.codigo_escola[:6]
                )

                entidade = entidades.get(entidade_codigo)

                if not entidade:
                    raise Exception(
                        f"Entidade não encontrada: {entidade_codigo}"
                    )

                responsavel = responsaveis.get(
                    item.responsavel.cpf
                )

                divida = dividas.get(item.codigo_carne)

                if divida:

                    divida.numeroCobranca = item.numero_carne
                    divida.responsavel = responsavel
                    divida.tipoCobranca = tipo_cobranca
                    divida.dataVencimento = item.data_vencimento
                    divida.valorCobranca = item.valor
                    divida.valorMulta = item.multa
                    divida.codigoAluno = item.codigo_aluno
                    divida.percentualMulta = item.percentual_multa
                    divida.percentualJuros = item.percentual_juro
                    divida.serie = item.serie_turma
                    divida.nomeAluno = item.aluno_nome
                    divida.entidade = entidade
                    divida.escola = item.escola

                    divida.save()

                    atualizados += 1

                else:

                    nova = Divida.objects.create(
                        codigoCobranca=item.codigo_carne,
                        numeroCobranca=item.numero_carne,
                        responsavel=responsavel,
                        tipoCobranca=tipo_cobranca,
                        dataVencimento=item.data_vencimento,
                        valorCobranca=item.valor,
                        valorMulta=item.multa,
                        codigoAluno=item.codigo_aluno,
                        percentualMulta=item.percentual_multa,
                        percentualJuros=item.percentual_juro,
                        serie=item.serie_turma,
                        nomeAluno=item.aluno_nome,
                        entidade=entidade,
                        escola=item.escola,
                    )

                    dividas[item.codigo_carne] = nova

                    criados += 1

            except Exception as e:
                erros += 1
                print(
                    f"Erro no Codigo {item.codigo_carne}: {e}"
                )

        return Response({
            "criados": criados,
            "atualizados": atualizados,
            "erros": erros
        })


CPF_REGEX = re.compile(r"/D")

IDX_ESCOLA = 1
IDX_CPF = 2
IDX_NOME = 3
IDX_RG = 4
IDX_ENDERECO = 5
IDX_NUMERO_CASA = 6
IDX_BAIRRO = 8
IDX_CIDADE = 9
IDX_UF = 10
IDX_CEP = 11
IDX_TELEFONES = 12
IDX_NUMERO_COBRANCA = 15
IDX_DATA_VENCIMENTO = 16
IDX_VALOR = 17
IDX_CODIGO_ALUNO = 18
IDX_NOME_ALUNO = 19
IDX_SERIE = 20


def limpar_cpf(value):
    return CPF_REGEX.sub("", value or "")

def formatar_data(data_str):
    if not data_str:
        return None

    return datetime.datetime.strptime(
        data_str,
        "%d/%m/%Y"
    ).date()

def formatar_valor(valor):
    if not valor:
        return None

    valor = valor.replace(".", "").replace(",", ".")
    return Decimal(valor)


def formata_serie(turma_string):
    if not turma_string:
        return ""

    turma_string = turma_string.lower()

    return (
        turma_string
        .replace("turma:", "")
        .strip()[:20]
    )


class ImportCsvView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "Arquivo não enviado"},
                status=400,
            )

        decoded = io.TextIOWrapper(
            file.file,
            encoding="utf-8"
        )

        reader = csv.reader(decoded, delimiter=";")

        next(reader, None)

        erros = []

        responsaveis_sucesso = 0
        dividas_sucesso = 0

        novos_responsaveis = {}
        novas_dividas = []

        entidade = Entidade.objects.get(codigo="123456") # Codigo do Grupo Objetivo

        escolas_cache = {
            e.codigo: e
            for e in Escola.objects.filter(entidade=entidade)
        }

        rows = list(reader)

        cpfs = {
            limpar_cpf(row[IDX_CPF])
            for row in rows
            if row[IDX_CPF]
        }

        responsaveis_cache = {
            r.cpf: r
            for r in Responsavel.objects.filter(
                entidade=entidade,
                cpf__in=cpfs
            )
        }

        with transaction.atomic():

            for i, row in enumerate(rows, start=1):

                try:

                    cpf = limpar_cpf(row[IDX_CPF])

                    if not cpf:
                        raise ValueError("CPF vazio")

                    obj = Responsavel(
                        nome=row[IDX_NOME],
                        cpf=row[IDX_CPF],
                        rg=row[IDX_RG],
                        endereco=row[IDX_ENDERECO],
                        complemento=row[IDX_NUMERO_CASA],
                        bairro=row[IDX_BAIRRO],
                        cidade=row[IDX_CIDADE],
                        uf=row[IDX_UF],
                        cep=row[IDX_CEP],
                        telefones=row[IDX_TELEFONES],
                        entidade=entidade,
                    )

                    key = (entidade.id, cpf)

                    novos_responsaveis[key] = obj

                    responsaveis_sucesso += 1

                except Exception as e:

                    erros.append({
                        "linha": i,
                        "erro": str(e),
                    })

            Responsavel.objects.bulk_create(
                novos_responsaveis.values(),
                update_conflicts=True,
                unique_fields=["entidade", "cpf"],
                update_fields=[
                    "nome",
                    "rg",
                    "endereco",
                    "complemento",
                    "bairro",
                    "cidade",
                    "uf",
                    "cep",
                    "telefones",
                ],
                batch_size=1000
            )

            responsaveis_cache = {
                r.cpf: r
                for r in Responsavel.objects.filter(
                    entidade=entidade,
                    cpf__in=cpfs
                )
            }



            for i, row in enumerate(rows, start=1):

                try:

                    cpf = limpar_cpf(row[IDX_CPF])

                    responsavel = responsaveis_cache.get(cpf)

                    if not responsavel:
                        raise ValueError(
                            f"Responsável não encontrado: {cpf}"
                        )

                    escola = escolas_cache.get(
                        row[IDX_ESCOLA]
                    )

                    if not escola:
                        raise ValueError(
                            f"Escola não encontrada: {row[IDX_ESCOLA]}"
                        )

                    numero_cobranca = row[IDX_NUMERO_COBRANCA]

                    if not numero_cobranca:
                        raise ValueError(
                            "Número da cobrança vazio"
                        )


                    obj = Divida(
                        entidade=entidade,
                        responsavel=responsavel,
                        responsavelAtual=responsavel,
                        tipoCobranca_id=1,
                        numeroCobranca=numero_cobranca,
                        dataVencimento=formatar_data(
                            row[IDX_DATA_VENCIMENTO]
                        ),
                        valorCobranca=formatar_valor(
                            row[IDX_VALOR]
                        ),
                        escola=escola,
                        nomeAluno=row[IDX_NOME_ALUNO],
                        codigoAluno=row[IDX_CODIGO_ALUNO],
                        serie=formata_serie(
                            row[IDX_SERIE]
                        ),
                    )

                    novas_dividas.append(obj)

                    dividas_sucesso += 1

                except Exception as e:

                    erros.append({
                        "linha": i,
                        "erro": str(e),
                    })

            Divida.objects.bulk_create(
                novas_dividas,
                update_conflicts=True,
                unique_fields=[
                    "numeroCobranca",
                    "entidade",
                ],
                update_fields=[
                    "responsavel",
                    "responsavelAtual",
                    "tipoCobranca",
                    "dataVencimento",
                    "valorCobranca",
                    "escola",
                    "nomeAluno",
                    "codigoAluno",
                    "serie",
                ],
                batch_size=1000
            )

        return Response({
            "responsaveis-importados": responsaveis_sucesso,
            "dividas-importadas": dividas_sucesso,
            "erros": erros
        }, status=status.HTTP_200_OK)
