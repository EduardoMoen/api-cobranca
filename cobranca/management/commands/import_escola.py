import csv
from django.core.management.base import BaseCommand
from cobranca.models import Escola


class Command(BaseCommand):
    help = "Importa Escola do CSV"

    def handle(self, *args, **kwargs):

        with open("escola.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")

            for row in reader:
                if not row:
                    continue

                Escola.objects.create(
                    id=str(row[0]),
                    codigo=str(row[2]),
                    nome=str(row[3]),
                    endereco=str(row[4]),
                    bairro=str(row[5]),
                    cidade=str(row[6]),
                    uf=str(row[7][:2]),
                    cep=str(row[8]),
                    email=str(row[9]),
                    obs=str(row[10]),
                    entidade_id=str(row[11])
                )

        self.stdout.write(self.style.SUCCESS("Importação concluída"))
