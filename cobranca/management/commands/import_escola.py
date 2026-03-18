import csv
from django.core.management.base import BaseCommand
from cobranca.models import Escola


class Command(BaseCommand):
    help = "Importa Escola do CSV"

    @staticmethod
    def add_none(value):
        if value is None:
            return None

        if value.upper() == "NULL":
            return None

        return value

    def handle(self, *args, **kwargs):

        with open("escola.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")

            for row in reader:
                if not row:
                    continue

                Escola.objects.create(
                    id=self.add_none(row[0]),
                    codigo=self.add_none(row[2]),
                    nome=self.add_none(row[3]),
                    endereco=self.add_none(row[4]),
                    bairro=self.add_none(row[5]),
                    cidade=self.add_none(row[6]),
                    uf=self.add_none(row[7][:2]),
                    cep=self.add_none(row[8]),
                    email=self.add_none(row[9]),
                    obs=self.add_none(row[10]),
                    entidade_id=self.add_none(row[11])
                )

        self.stdout.write(self.style.SUCCESS("Importação concluída"))
