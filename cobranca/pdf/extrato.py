from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

def gerar_extrato_pdf(responsavel, dividas):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
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
        elements.append(Paragraph("Extrato do Aluno", styles["Title"]))
        elements.append(Spacer(1, 0.3 * inch))

        # Informações
        elements.append(Paragraph(f"Escola: {escola.nome}", styles["Normal"]))
        elements.append(Paragraph(f"Aluno: {nome_aluno}", styles["Normal"]))
        elements.append(
            Paragraph(f"Responsável: {responsavel.nome} - CPF: {responsavel.cpf}",
                      styles["Normal"]
            )
        )

        elements.append(Spacer(1, 0.5 * inch))

        #Tabela
        data = [["Código", "Vencimento", "Valor"]]

        for divida in lista_dividas:
            data.append([
                divida.numeroCobranca,
                divida.dataVencimento.strftime("%d/%m/%Y"),
                f"R$ {divida.valorCobranca:.2f}",
            ])

        table = Table(data)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (2, 1), (2, -1), "RIGHT"),
        ]))

        elements.append(table)

        #Total do aluno
        valor_total_aluno = sum(d.valorCobranca for d in lista_dividas)

        elements.append(Spacer(1, 0.2 * inch))
        elements.append(
            Paragraph(
                f"<b>Total do Aluno:</b> R$ {valor_total_aluno:.2f}",
                styles["Normal"],
            )
        )

        if contador < total_alunos:
            elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)

    return buffer
