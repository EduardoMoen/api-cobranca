import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from cobranca.models import Indice


class Command(BaseCommand):
    help = "Importa Bancos do CSV"

    def handle(self, *args, **kwargs):

        with open("indices.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")

            for row in reader:
                if not row:
                    continue

                Indice.objects.create(
                    ano=int(row[0]),
                    mes=int(row[2]),
                    indice=Decimal(row[3]),
                )

        self.stdout.write(self.style.SUCCESS("Importação concluída"))