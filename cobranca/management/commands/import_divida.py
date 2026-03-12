import csv
from django.core.management.base import BaseCommand
from cobranca.models import Divida
from decimal import Decimal, InvalidOperation

class Command(BaseCommand):
    help = "Importa divida do CSV"

    def parse_decimal(self, value):
        if value  in ("NULL", "", None):
            return None

        value = value.replace(".", "").replace(",", ".")

        try:
            return Decimal(value)
        except InvalidOperation:
            return None

    def parse_int(self, value):
        if value in ("NULL", "", None):
            return None
        return int(value)

    def handle(self, *args, **kwargs):

        with open("divida.csv", encoding="utf-8-sig") as file:
            reader = csv.reader(file, delimiter=";")

            batch = []

            for row in reader:
                if not row:
                    continue

                batch.append(
                    Divida(
                        id=str(row[0]),
                        entidade_id=str(row[1]),
                        responsavel_id=str(row[2]),
                        tipoCobranca_id=self.parse_int(row[3]),
                        numeroCobranca=str(row[4]),
                        dataPrimeiraImportacao=None if row[5] == "NULL" else row[5].split(" ")[0],
                        dataUltimaImportacao=None if row[6] == "NULL" else row[6].split(" ")[0],
                        # banco=int(row[6]),
                        agencia=str(row[7]),
                        conta=str(row[8]),
                        alinea_id=self.parse_int(row[9]),
                        dataVencimento=None if row[10] == "NULL" else row[10].split(" ")[0],
                        valorCobranca=self.parse_decimal(row[11]),
                        valorCobrancaAcao=self.parse_decimal(row[12]),
                        # statusValorAcao=bool(row[21]),
                        parcela=str(row[13]),
                        valorMulta=self.parse_decimal(row[14]),
                        valorJuro=self.parse_decimal(row[15]),
                        dataAcertoMantenedora=None if row[16] == "NULL" else row[16].split(" ")[0],
                        valorPago=self.parse_decimal(row[17]),
                        numeroContrato=str(row[18]),
                        responsavelAtual_id=str(row[19]),
                        # statusBolsista=bool(row[6]),
                        # statusEstornado=bool(row[7]),
                        codigoAluno=self.parse_int(row[20]),
                        nomeAluno=str(row[21]),
                        serie=str(row[22]),
                        escola_id=str(row[23]),
                        ano=self.parse_int(row[24]),
                        dataInicioJuro=None if row[25] == "NULL" else row[25].split(" ")[0],
                        dataAcertoJw=None if row[26] == "NULL" else row[26].split(" ")[0],
                        numeroDias=self.parse_int(row[27]),
                        mesInicioCorrecao=self.parse_int(row[28]),
                        anoInicioCorrecao=self.parse_int(row[29]),
                        # indiceInicial=self.parse_decimal(row[30]),
                        mesFimCorrecao=self.parse_int(row[31]),
                        anoFimCorrecao=self.parse_int(row[32]),
                        # indiceFinal=self.parse_decimal(row[33]),
                        valorCorrigido=self.parse_decimal(row[34]),
                        percentualMulta=self.parse_decimal(row[35]),
                        valorMultaJw=self.parse_decimal(row[36]),
                        percentualJuros=self.parse_decimal(row[37]),
                        valorJuroJw=self.parse_decimal(row[38]),
                        valorSubtotal=self.parse_decimal(row[39]),
                        percentualHonorarios=self.parse_decimal(row[40]),
                        valorHonorarios=self.parse_decimal(row[41]),
                        valorTotal=self.parse_decimal(row[42]),
                        # statusPagoJw=bool(row[19]),
                        dataPagoJw=None if row[43] == "NULL" else row[43].split(" ")[0],
                        valorCobrado=self.parse_decimal(row[44]),
                        numeroRecibo=self.parse_int(row[45]),
                        dataImpressaoCarta=None if row[46] == "NULL" else row[46].split(" ")[0],
                        nomeResponsavelCobranca=str(row[47]),
                        posicaoContrato_id=str(row[48]),
                        posicaoCheque_id=str(row[49]),
                        andamento_id=str(row[50]),
                        lugar_id=str(row[51]),
                        # statusAcao=bool(row[22]),
                        # statusSpcNaoEnviar=bool(row[1]),
                        pasta=str(row[52]),
                        numeroVara=str(row[53]),
                        numeroProcesso=str(row[54]),
                        dataAcao=None if row[55] == "NULL" else row[55].split(" ")[0],
                        # statusNaoEnviarCarta=bool(row[8]),
                        # statusAcordo=bool(row[9]),
                        dataResponsavelCobranca=None if row[56] == "NULL" else row[56].split(" ")[0],
                        dataSpcEnvio=None if row[57] == "NULL" else row[57].split(" ")[0],
                        statusSpcEnvio=str(row[58]),
                        dataSpcBaixa=None if row[59] == "NULL" else row[59].split(" ")[0],
                        statusSpcBaixa=str(row[60]),
                        # statusSpcBaixaManual=bool(row[4]),
                        # statusSpcBaixar=bool(row[5]),
                        remessaSpcEnvio=self.parse_int(row[61]),
                        remessaSpcBaixa=self.parse_int(row[62]),
                        dataAcertoJwMantenedora=None if row[63] == "NULL" else row[63].split(" ")[0],
                        obsJw=str(row[64]),
                        # acordo=str(row[10]),
                    )
                )

                if len(batch) >= 1000:
                    Divida.objects.bulk_create(batch, batch_size=1000)
                    batch = []
            if batch:
                Divida.objects.bulk_create(batch, batch_size=1000)

        self.stdout.write(self.style.SUCCESS("Importação concluída"))
