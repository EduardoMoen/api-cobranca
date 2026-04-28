import requests
import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.db import transaction, IntegrityError
from rest_framework.response import Response

from cobranca.serializers import ResponsavelImportacaoSerializer


def get_external_data(page_size: int):
    # url = f"https://7edu-br-accountsreceiving-staging-api.educadventista.org/api/v2/cobrancas/boletos/?PageSize={page_size}"
    url = f"https://7edu-br-accountsreceiving-api.educadventista.org/api/v2/cobrancas/boletos/?PageSize={page_size}"


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
    # url = f"https://7edu-br-accountsreceiving-staging-api.educadventista.org/api/v2/cobrancas/responsaveis/?PageSize={page_size}"
    url = f"https://7edu-br-accountsreceiving-api.educadventista.org/api/v2/cobrancas/responsaveis/?PageSize={page_size}"


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
    # url = f"https://7edu-br-accountsreceiving-staging-api.educadventista.org/api/v2/cobrancas/responsaveis-com-boletos/?PageSize={page_size}"
    url = f"https://7edu-br-accountsreceiving-api.educadventista.org/api/v2/cobrancas/responsaveis-com-boletos/?PageSize={page_size}"


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
