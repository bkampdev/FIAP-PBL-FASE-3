"""Gera relatorio.pdf a partir da fonte Markdown. Requer reportlab."""

import re
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate


PASTA = Path(__file__).resolve().parents[1] / "relatorio"
AZUL = colors.HexColor("#133B56")
TEXTO = colors.HexColor("#253746")


def formatar_inline(texto):
    texto = escape(texto)
    texto = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', texto)
    return re.sub(
        r"\[([^\]]+)\]\((https://[^\s)]+)\)",
        r'<link href="\2" color="#006C88"><u>\1</u></link>',
        texto,
    )


def rodape(canvas, documento):
    largura, _ = documento.pagesize
    esquerda = documento.leftMargin
    direita = largura - documento.rightMargin
    canvas.setStrokeColor(colors.HexColor("#B4C9D1"))
    canvas.line(esquerda, 44, direita, 44)
    canvas.setFillColor(AZUL)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(esquerda, 29, "FIAP PBL | Fase 3")
    canvas.drawRightString(direita, 29, str(documento.page))


def gerar():
    fonte = (PASTA / "relatorio.md").read_text(encoding="utf-8")
    corpo = ParagraphStyle(
        "Corpo", fontName="Helvetica", fontSize=11, leading=15,
        textColor=TEXTO, spaceAfter=8,
    )
    titulo = ParagraphStyle(
        "Título", parent=corpo, fontName="Helvetica-Bold", fontSize=28,
        leading=32, textColor=AZUL, spaceAfter=6, keepWithNext=True,
    )
    subtitulo = ParagraphStyle(
        "Subtítulo", parent=corpo, fontSize=11, textColor=AZUL,
        spaceAfter=15, keepWithNext=True,
    )
    secao = ParagraphStyle(
        "Seção", parent=corpo, fontName="Helvetica-Bold", fontSize=14,
        leading=17, textColor=AZUL, spaceBefore=7, keepWithNext=True,
    )

    paragrafos = []
    for indice, bloco in enumerate(re.split(r"\n\s*\n", fonte.strip())):
        estilo = corpo
        if bloco.startswith("# "):
            bloco, estilo = bloco[2:], titulo
        elif bloco.startswith("## "):
            bloco, estilo = bloco[3:], secao
        elif indice == 1:
            estilo = subtitulo
        paragrafos.append(Paragraph(formatar_inline(bloco), estilo))

    documento = SimpleDocTemplate(
        str(PASTA / "relatorio.pdf"),
        pagesize=A4,
        leftMargin=53,
        rightMargin=53,
        topMargin=49,
        bottomMargin=62,
        title="Sistemas da Colônia Aurora",
        author="Equipe Colônia Aurora",
        invariant=True,
    )
    documento.build(paragrafos, onFirstPage=rodape, onLaterPages=rodape)


if __name__ == "__main__":
    gerar()
