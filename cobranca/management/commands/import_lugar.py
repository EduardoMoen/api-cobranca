import csv
from django.core.management.base import BaseCommand
from cobranca.models import Lugar


class Command(BaseCommand):
    help = "Importa Lugar do CSV"

    def handle(self, *args, **kwargs):

        with open("lugar.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")

            for row in reader:
                if not row:
                    continue

                Lugar.objects.create(
                    id=str(row[0]),
                    nome=str(row[1]),
                    escritorio_id=str(row[2]),
                )

        self.stdout.write(self.style.SUCCESS("Importação concluída"))
