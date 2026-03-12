import csv
from django.core.management.base import BaseCommand
from cobranca.models import Andamento


class Command(BaseCommand):
    help = "Importa Andamento do CSV"

    def handle(self, *args, **kwargs):

        with open("andamento.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")

            for row in reader:
                if not row:
                    continue

                Andamento.objects.create(
                    id=str(row[0]),
                    nome=str(row[1]),
                    escritorio_id=str(row[2])
                )

        self.stdout.write(self.style.SUCCESS("Importação concluída"))
