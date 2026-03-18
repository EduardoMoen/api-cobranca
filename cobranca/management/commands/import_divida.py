import csv
from django.core.management.base import BaseCommand
from cobranca.models import Divida
from decimal import Decimal, InvalidOperation

class Command(BaseCommand):
    help = "Importa divida do CSV"

    @staticmethod
    def bool_fields(value):
        if str(value) == "1":
            return True

        return False

    @staticmethod
    def add_str_none(value):
        if value is None:
            return None

        if value.upper() == "NULL":
            return None

        return str(value)

    @staticmethod
    def indices_fields(value):
        if value in ("NULL", "", None):
            return None

        return Decimal(value)

    @staticmethod
    def parse_decimal(value):
        if value  in ("NULL", "", None):
            return None

        value = value.replace(".", "").replace(",", ".")

        try:
            return Decimal(value)
        except InvalidOperation:
            return None

    @staticmethod
    def parse_int(value):
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
                        id=self.add_str_none(row[0]),
                        entidade_id=self.add_str_none(row[1]),
                        responsavel_id=self.add_str_none(row[2]),
                        tipoCobranca_id=self.parse_int(row[3]),
                        numeroCobranca=self.add_str_none(row[4]),
                        dataPrimeiraImportacao=None if row[5] == "NULL" else row[5].split(" ")[0],
                        dataUltimaImportacao=None if row[6] == "NULL" else row[6].split(" ")[0],
                        banco_id=self.parse_int(row[7]),
                        agencia=self.add_str_none(row[8]),
                        conta=self.add_str_none(row[9]),
                        alinea_id=self.parse_int(row[10]),
                        dataVencimento=None if row[11] == "NULL" else row[11].split(" ")[0],
                        valorCobranca=self.parse_decimal(row[12]),
                        valorCobrancaAcao=self.parse_decimal(row[13]),
                        statusValorAcao=self.bool_fields(row[14]),
                        parcela=self.add_str_none(row[15]),
                        valorMulta=self.parse_decimal(row[16]),
                        valorJuro=self.parse_decimal(row[17]),
                        dataAcertoMantenedora=None if row[18] == "NULL" else row[18].split(" ")[0],
                        valorPago=self.parse_decimal(row[19]),
                        numeroContrato=self.add_str_none(row[20]),
                        responsavelAtual_id=self.add_str_none(row[21]),
                        statusBolsista=self.bool_fields(row[22]),
                        statusEstornado=self.bool_fields(row[23]),
                        codigoAluno=self.parse_int(row[24]),
                        nomeAluno=self.add_str_none(row[25]),
                        serie=self.add_str_none(row[26]),
                        escola_id=self.add_str_none(row[27]),
                        ano=self.parse_int(row[28]),
                        dataInicioJuro=None if row[29] == "NULL" else row[29].split(" ")[0],
                        dataAcertoJw=None if row[30] == "NULL" else row[30].split(" ")[0],
                        numeroDias=self.parse_int(row[31]),
                        mesInicioCorrecao=self.parse_int(row[32]),
                        anoInicioCorrecao=self.parse_int(row[33]),
                        indiceInicial=self.indices_fields(row[34]),
                        mesFimCorrecao=self.parse_int(row[35]),
                        anoFimCorrecao=self.parse_int(row[36]),
                        indiceFinal=self.indices_fields(row[37]),
                        valorCorrigido=self.parse_decimal(row[38]),
                        percentualMulta=self.parse_decimal(row[39]),
                        valorMultaJw=self.parse_decimal(row[40]),
                        percentualJuros=self.parse_decimal(row[41]),
                        valorJuroJw=self.parse_decimal(row[42]),
                        valorSubtotal=self.parse_decimal(row[43]),
                        percentualHonorarios=self.parse_decimal(row[44]),
                        valorHonorarios=self.parse_decimal(row[45]),
                        valorTotal=self.parse_decimal(row[46]),
                        statusPagoJw=self.bool_fields(row[47]),
                        dataPagoJw=None if row[48] == "NULL" else row[48].split(" ")[0],
                        valorCobrado=self.parse_decimal(row[49]),
                        numeroRecibo=self.parse_int(row[50]),
                        dataImpressaoCarta=None if row[51] == "NULL" else row[51].split(" ")[0],
                        nomeResponsavelCobranca=self.add_str_none(row[52]),
                        posicaoContrato_id=self.add_str_none(row[53]),
                        posicaoCheque_id=self.add_str_none(row[54]),
                        andamento_id=self.add_str_none(row[55]),
                        lugar_id=self.add_str_none(row[56]),
                        statusAcao=self.bool_fields(row[57]),
                        statusSpcNaoEnviar=self.bool_fields(row[58]),
                        pasta=self.add_str_none(row[59]),
                        numeroVara=self.add_str_none(row[60]),
                        numeroProcesso=self.add_str_none(row[61]),
                        dataAcao=None if row[62] == "NULL" else row[62].split(" ")[0],
                        statusNaoEnviarCarta=self.bool_fields(row[63]),
                        statusAcordo=self.bool_fields(row[64]),
                        dataResponsavelCobranca=None if row[65] == "NULL" else row[65].split(" ")[0],
                        dataSpcEnvio=None if row[66] == "NULL" else row[66].split(" ")[0],
                        statusSpcEnvio=self.add_str_none(row[67]),
                        dataSpcBaixa=None if row[68] == "NULL" else row[68].split(" ")[0],
                        statusSpcBaixa=self.add_str_none(row[69]),
                        statusSpcBaixaManual=self.bool_fields(row[70]),
                        statusSpcBaixar=self.bool_fields(row[71]),
                        remessaSpcEnvio=self.parse_int(row[72]),
                        remessaSpcBaixa=self.parse_int(row[73]),
                        dataAcertoJwMantenedora=None if row[74] == "NULL" else row[74].split(" ")[0],
                        obsJw=self.add_str_none(row[75]),
                        statusCancelado=self.bool_fields(row[76]),
                        # acordo=str(row[10]),
                    )
                )

                if len(batch) >= 1000:
                    Divida.objects.bulk_create(batch, batch_size=1000)
                    batch = []
            if batch:
                Divida.objects.bulk_create(batch, batch_size=1000)

        self.stdout.write(self.style.SUCCESS("Importação concluída"))
