import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from io import BytesIO


def gerar_carta_pdf(responsavel, dividas):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        name="Titulo",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        spaceAfter=10,
    )

    texto_style = ParagraphStyle(
        name="Texto",
        parent=styles["Normal"],
        alignment=TA_LEFT,
        # spaceAfter=10,
    )

    assinatura_style = ParagraphStyle(
        name="Assinatura",
        parent=styles["Normal"],
        alignment=TA_RIGHT,
        spaceAfter=30,
    )

    elements = []

    # TEXTOS
    texto1 = f"""
        Pela presente comunicamos V.Sa. que, encontra-se em aberto o pagamento da(s) mensalidade(s)
        de seu filho(a) matriculado(a) no(a) Unasp EC no ano de 2020, referente(s) aos boleto(s)
        vencido(s):
        """
    texto2 = f"""
        Tendo esgotado o prazo para pagamento no Banco Credenciado, V.Sa. deverá, dentro do prazo
        de 5 (cinco) dias, entrar em contato com o Escritório Jurídico, à Rua Barbosa da Cunha, 386 –
        Guanabara, Campinas/SP, que estará atendendo de segunda à sexta-feira das 9:00 às 12:00 h e
        das 13:00 às 17:00 h, ou pelo Fone (19) 3232-5767 e celulares corporativos (19) 98199-7126 e
        (19) 99392-1431.
        """
    texto3 = f"""
        Caso V. Sa. já tenha pago a(s) mensalidade(s) em questão, queira por gentileza, desconsiderar
        esta comunicação.
        """

    from collections import defaultdict
    dividas_por_aluno = defaultdict(list)

    for divida in dividas:
        dividas_por_aluno[divida.nomeAluno].append(divida)

    total_alunos = len(dividas_por_aluno)
    contador = 0

    for nome_aluno, lista_dividas in dividas_por_aluno.items():
        contador += 1

        numero_aluno = lista_dividas[0].codigoAluno

        if not lista_dividas:
            continue

        elements.append(Paragraph(f"Campinas, {datetime.date.today().strftime("%d/%m/%Y")}."))

        elements.append(Spacer(1, 20))

        elements.append(Paragraph(f"Ilmo(a). Sr(a)."))
        elements.append(Paragraph(f"{responsavel.nome}"))
        elements.append(Paragraph(f"Aluno: {nome_aluno} - {numero_aluno}"))
        elements.append(Paragraph(f"{responsavel.endereco} - {responsavel.bairro}"))
        elements.append(Paragraph(f"{responsavel.cep} {responsavel.cidade} - {responsavel.uf}"))

        elements.append(Spacer(1, 20))

        elements.append(Paragraph(texto1, texto_style))

        elements.append(Spacer(1, 20))

        texto4 = ""
        for divida in lista_dividas:
            texto4 += divida.numeroCobranca + ", "
        elements.append(Paragraph(f"{texto4[:-2]};"))

        elements.append(Spacer(1, 20))

        elements.append(Paragraph(texto2, texto_style))

        elements.append(Spacer(1, 20))

        elements.append(Paragraph(texto3, texto_style))

        elements.append(Spacer(1, 20))

        elements.append(Paragraph("Atenciosamente,"))

        elements.append(Spacer(1, 20))

        elements.append(Paragraph("Cremovale Cobranças e Serviços Ltda"))



        if contador < total_alunos:
            elements.append(PageBreak())


    doc.build(elements)

    buffer.seek(0)
    return buffer
