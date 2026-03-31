import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

def formatar_moeda(valor):
    valor = valor or 0
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def cabecalho(canvas, doc):
    canvas.saveState()
    width, height = doc.pagesize

    try:
        logo = ImageReader("cobranca/pdf/logo/cremovale_logo.jpeg")
        canvas.drawImage(
            logo,
            30,
            height - 100,
            width=100,
            height=100,
            preserveAspectRatio=True,
            mask="auto",
        )
    except:
        pass

        # 🏢 NOME DA EMPRESA
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawCentredString(width / 2, height - 40, "CREMOVALE COBRANÇAS E SERVIÇOS LTDA")
    canvas.drawCentredString(width / 2, height - 70, "Extrato de Débitos")

    # Linha do header
    canvas.setStrokeColor(colors.grey)
    canvas.line(30, height - 85, width - 30, height - 85)

    # 🔻 RODAPÉ
    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(width / 2, 20, f"Rua Barbosa da Cunha, 386 - Guanabara, Campinas / SP - CEP. 13.073-320")
    canvas.drawCentredString(width / 2, 10, f"Fone: (0XX19) 3232-5767")

    # canvas.drawRightString(width - 30, 20, f"Página {doc.page}")

    canvas.restoreState()



def gerar_extrato_pdf(responsavel, dividas):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()

    from collections import defaultdict
    dividas_por_aluno = defaultdict(list)

    for divida in dividas:
        dividas_por_aluno[divida.nomeAluno].append(divida)

    total_alunos = len(dividas_por_aluno)
    contador = 0

    for nome_aluno, lista_dividas in dividas_por_aluno.items():
        contador += 1

        if not lista_dividas:
            continue

        escola = lista_dividas[0].escola

        #Título
        elements.append(Spacer(1, 0.4 * inch))

        info_style = ParagraphStyle(
            "info_style",
            parent=styles["Normal"],
            fontSize=12,  # 👈 muda aqui
            leading=15  # altura da linha (opcional)
        )

        # Informações
        elements.append(Paragraph(f"<b>CPF:</b> {responsavel.cpf}", info_style))
        elements.append(Paragraph(f"<b>Responsável:</b> {responsavel.nome}", info_style))
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph(f"<b>Escola:</b> {escola.nome} - {escola.codigo}", info_style))
        elements.append(Paragraph(f"<b>Aluno:</b> {nome_aluno}", info_style))

        elements.append(Spacer(1, 0.5 * inch))

        elements.append(
            Paragraph(
                f"<b>Atualizado até:</b> {dividas[0].dataAcertoJw.strftime("%d/%m/%Y")}",
                styles["Normal"],
            )
        )

        elements.append(Spacer(1, 0.2 * inch))

        #Tabela
        data = [["Docto", "Ano", "Parcela", "Valor", "Vencimento", "Corrigido", "Indice", "Multa", "%", "Juros", "%", "Honorarios", "Total"]]

        total_valor = 0
        total_corrigido = 0
        total_multa = 0
        total_juros = 0
        total_honorarios = 0
        total_valor_final = 0

        for divida in lista_dividas:
            total_valor += divida.valorCobranca or 0
            total_corrigido += divida.valorCorrigido or 0
            total_multa += divida.valorMultaJw or 0
            total_juros += divida.valorJuroJw or 0
            total_honorarios += divida.valorHonorarios or 0
            total_valor_final += divida.valorTotal or 0

            data.append([
                divida.numeroCobranca,
                divida.anoInicioCorrecao,
                divida.parcela,
                f"{formatar_moeda(divida.valorCobranca)}",
                divida.dataVencimento.strftime("%d/%m/%Y"),
                f"{formatar_moeda(divida.valorCorrigido)}",
                f"{divida.indiceInicial:.6f}",
                divida.valorMultaJw,
                f"{divida.percentualMulta:.1f}",
                f"{formatar_moeda(divida.valorJuroJw)}",
                f"{divida.percentualJuros:.1f}",
                f"{formatar_moeda(divida.valorHonorarios)}",
                f"{formatar_moeda(divida.valorTotal)}",
            ])

        data.append([
            "TOTAIS",
            "",
            "",
            f"{formatar_moeda(total_valor)}",
            "",
            f"{formatar_moeda(total_corrigido)}",
            "",
            f"{formatar_moeda(total_multa)}",
            "",
            f"{formatar_moeda(total_juros)}",
            "",
            f"{formatar_moeda(total_honorarios)}",
            f"{formatar_moeda(total_valor_final)}",
        ])

        table = Table(data)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))

        elements.append(table)

        #Total do aluno
        valor_total_aluno = sum(d.valorCobranca for d in lista_dividas)

        elements.append(Spacer(1, 0.2 * inch))
        elements.append(
            Paragraph(
                f"<b>Impresso em:</b> {datetime.date.today().strftime("%d/%m/%Y")}",
                styles["Normal"],
            )
        )

        if contador < total_alunos:
            elements.append(PageBreak())

    doc.build(
        elements,
        onFirstPage=cabecalho,
    )
    buffer.seek(0)

    return buffer
