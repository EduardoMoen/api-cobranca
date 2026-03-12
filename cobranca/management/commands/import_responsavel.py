import csv
from django.core.management.base import BaseCommand
from cobranca.models import Responsavel

class Command(BaseCommand):
    help = "Importa Responsável do CSV"

    def handle(self, *args, **kwargs):

        with open("responsavel.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")

            batch = []

            for row in reader:
                if not row:
                    continue

                batch.append(
                    Responsavel(
                        id=str(row[0]),
                        cpf=str(row[20]),
                        nome=str(row[19]),
                        nascimento = None if row[2] == "NULL" else row[2].split(" ")[0],
                        endereco=str(row[3]),
                        complemento=str(row[4]),
                        bairro=str(row[5]),
                        cidade=str(row[6]),
                        uf=str(row[7][:2]),
                        cep=str(row[8]),
                        rg=str(row[9]),
                        rg_emissao=str(row[10]),
                        estado_civil=str(row[22]),
                        # telefones=str(row[1]),
                        entidade_id=str(row[21]),
                    )
                )

                if len(batch) >= 1000:
                    Responsavel.objects.bulk_create(batch, batch_size=1000)
                    batch = []
            if batch:
                Responsavel.objects.bulk_create(batch, batch_size=1000)

        self.stdout.write(self.style.SUCCESS("Importação concluída"))
