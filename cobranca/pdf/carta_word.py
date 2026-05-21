import datetime
from io import BytesIO
from collections import defaultdict
from textwrap import dedent

from docx import Document
from docx.shared import Inches, Pt, Mm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


def gerar_carta_word(responsavel, dividas):

    document = Document()

    # MARGENS
    section = document.sections[0]

    section.page_width = Mm(210)
    section.page_height = Mm(297)

    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(20)
    section.right_margin = Mm(20)

    #RODAPÉ
    footer = section.footer

    p_footer = footer.paragraphs[0]

    p_footer.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    run = p_footer.add_run(
        "Rua Barbosa da Cunha, 386 - Guanabara, Campinas/SP - CEP 13.073-320\n"
        "Fone: (19) 3232-5767"
    )

    run.font.size = Pt(9)

    # TEXTOS
    texto1 = dedent("""
    Pela presente comunicamos V.Sa. que, encontra-se em aberto o pagamento da(s) mensalidade(s) de seu filho(a) matriculado(a) no(a) Unasp EC no ano de 2020, referente(s) aos boleto(s) vencido(s):
    """)

    texto2 = dedent("""
    Tendo esgotado o prazo para pagamento no Banco Credenciado, V.Sa. deverá, dentro do prazo de 5 (cinco) dias, entrar em contato com o Escritório Jurídico, à Rua Barbosa da Cunha, 386 – Guanabara, Campinas/SP.
    """)

    texto3 = dedent("""
    Caso V. Sa. já tenha pago a(s) mensalidade(s) em questão, queira por gentileza, desconsiderar esta comunicação.
    """)

    dividas_por_aluno = defaultdict(list)

    for divida in dividas:
        dividas_por_aluno[divida.nomeAluno].append(divida)

    total_alunos = len(dividas_por_aluno)
    contador = 0

    for nome_aluno, lista_dividas in dividas_por_aluno.items():

        contador += 1

        numero_aluno = lista_dividas[0].codigoAluno

        # LOGO
        try:
            document.add_picture(
                "cobranca/pdf/logo/logo_carta.jpeg",
                width=Inches(1.2)
            )
        except:
            pass

        # DATA
        p = document.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        p.add_run(
            f"Campinas, {datetime.date.today().strftime('%d/%m/%Y')}."
        )

        document.add_paragraph()

        p = document.add_paragraph()
        p.add_run("Ilmo(a). Sr(a).\n")
        p.add_run(responsavel.nome + "\n")
        p.add_run(
            f"Aluno: {nome_aluno} - {numero_aluno}\n"
        )
        p.add_run(
            f"{responsavel.endereco} - {responsavel.bairro}\n"
        )
        p.add_run(
            f"{responsavel.cep} {responsavel.cidade} - {responsavel.uf}"
        )

        document.add_paragraph()

        p = document.add_paragraph(texto1)
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        boletos = ", ".join(
            [divida.numeroCobranca for divida in lista_dividas]
        )

        document.add_paragraph(boletos)

        p = document.add_paragraph(texto2)
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        p = document.add_paragraph(texto3)
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

        document.add_paragraph()
        document.add_paragraph()
        document.add_paragraph("Atenciosamente,")

        document.add_paragraph()
        document.add_paragraph()
        document.add_paragraph("Cremovale Cobranças e Serviços Ltda")

        # QUEBRA DE PÁGINA
        if contador < total_alunos:
            document.add_page_break()

    buffer = BytesIO()

    document.save(buffer)

    buffer.seek(0)

    return buffer