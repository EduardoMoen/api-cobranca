import requests
import os

def get_external_data():
    url = "https://7edu-br-accountsreceiving-staging-api.educadventista.org/api/v2/cobrancas/boletos"

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
