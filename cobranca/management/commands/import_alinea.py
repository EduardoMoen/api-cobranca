import csv
from django.core.management.base import BaseCommand
from cobranca.models import Alinea


class Command(BaseCommand):
    help = "Importa Alinea do CSV"

    def handle(self, *args, **kwargs):

        with open("alinea.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")

            for row in reader:
                if not row:
                    continue

                Alinea.objects.create(
                    id=int(row[0]),
                    nome=str(row[1]),
                )

        self.stdout.write(self.style.SUCCESS("Importação concluída"))