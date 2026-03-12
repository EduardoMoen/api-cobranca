import csv
from django.core.management.base import BaseCommand
from cobranca.models import Entidade


class Command(BaseCommand):
    help = "Importa Entidade do CSV"

    def handle(self, *args, **kwargs):

        with open("entidade.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")

            for row in reader:
                if not row:
                    continue

                Entidade.objects.create(
                    id=str(row[0]),
                    codigo=str(row[1]),
                    nome=str(row[2]),
                    escritorio_id=str(row[3])
                )

        self.stdout.write(self.style.SUCCESS("Importação concluída"))
