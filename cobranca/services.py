import requests
import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from decimal import Decimal
from django.db.models import Sum

from django.db import transaction, IntegrityError
from rest_framework.response import Response

from cobranca.models import Divida, Baixa, AcordoParcela
from cobranca.serializers import ResponsavelImportacaoSerializer


def get_external_data(page_size: int):
    url = f"https://7edu-br-accountsreceiving-staging-api.educadventista.org/api/v2/cobrancas/boletos/?PageSize={page_size}"
    # url = f"https://7edu-br-accountsreceiving-api.educadventista.org/api/v2/cobrancas/boletos/?PageSize={page_size}"


    token = os.getenv("API_TOKEN")

    headers = {
        "X-API-KEY": token,
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_responsaveis_api(page_size: int):
    url = f"https://7edu-br-accountsreceiving-staging-api.educadventista.org/api/v2/cobrancas/responsaveis/?PageSize={page_size}"
    # url = f"https://7edu-br-accountsreceiving-api.educadventista.org/api/v2/cobrancas/responsaveis/?PageSize={page_size}"


    token = os.getenv("API_TOKEN")

    headers = {
        "X-API-KEY": token,
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def importar_responsaveis_com_boletos(page_size: int):
    url = f"https://7edu-br-accountsreceiving-staging-api.educadventista.org/api/v2/cobrancas/responsaveis-com-boletos/?PageSize={page_size}"
    # url = f"https://7edu-br-accountsreceiving-api.educadventista.org/api/v2/cobrancas/responsaveis-com-boletos/?PageSize={page_size}"


    token = os.getenv("API_TOKEN")

    headers = {
        "X-API-KEY": token,
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def enviar_email():
    html_content = render_to_string("emails/email.html")

    email = EmailMultiAlternatives(
        subject="Teste envio email",
        body="Teste",
        to=["eduardodoerner@gmail.com"],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

def distribuir_parcela(parcela: AcordoParcela):
    valor_restante = parcela.valor

    dividas = Divida.objects.filter(
        acordo=parcela.acordo
    ).order_by("-dataVencimento")

    for divida in dividas:
        if valor_restante <= 0:
            break

        total_baixado = divida.baixas.aggregate(
            total=Sum("valor")
        )["total"] or Decimal(0)

        saldo = divida.valorCobranca - total_baixado

        if saldo <= 0:
            continue

        baixa = min(saldo, valor_restante)

        Baixa.objects.create(
            parcela=parcela,
            divida=divida,
            valor=baixa,
        )

        enviar_baixa_api(
            parcela=parcela,
            divida=divida,
            valor=baixa,
        )

        valor_restante -= baixa


def enviar_baixa_api(parcela: AcordoParcela, divida: Divida, valor: Decimal):
    url = "https://7edu-br-accountsreceiving-staging-api.educadventista.org/api/v2/cobrancas/boletos/recebidos/"
    # url = "https://7edu-br-accountsreceiving-api.educadventista.org/api/v2/cobrancas/boletos/recebidos/"

    token = os.getenv("API_TOKEN")

    headers = {
        "X-API-KEY": token,
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    payload = {
        "codigoCarne": divida.codigoCobranca,
        "multa": 0,
        "juros": 0,
        "honorario": 0,
        "valorNominal": str(valor),
        "valorPago": str(valor),
        "descontoPago": 0,
        "correcaoMonetaria": 0,
        "numeroRecibo": f"{parcela.id}"
    }

    response = requests.post(url=url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
