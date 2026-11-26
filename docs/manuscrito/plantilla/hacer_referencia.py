"""Plantilla de Word (reference-doc de pandoc) con el formato de la guía UNI para el informe de Seminario de Tesis.

Uso: python hacer_referencia.py <carpeta_base> <salida.docx>. La carpeta base es la plantilla por defecto de pandoc
descomprimida (docs/manuscrito/plantilla/base).
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

base = Path(sys.argv[1])          # carpeta con la plantilla de pandoc descomprimida
salida = Path(sys.argv[2])        # .docx de referencia resultante

TNR = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman" />'

def estilo(style_id, nombre, ppr, rpr, extra=""):
    return (f'<w:style w:type="paragraph" w:styleId="{style_id}"><w:name w:val="{nombre}" />'
            f'<w:basedOn w:val="Normal" />{extra}<w:qFormat /><w:pPr>{ppr}</w:pPr><w:rPr>{rpr}</w:rPr></w:style>')

nuevos = {
    "Normal": '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal" /><w:qFormat />'
              '<w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="auto" /><w:jc w:val="both" /></w:pPr>'
              f'<w:rPr>{TNR}<w:sz w:val="24" /><w:szCs w:val="24" /></w:rPr></w:style>',
    "BodyText": estilo("BodyText", "Body Text", '<w:spacing w:before="0" w:after="240" w:line="360" w:lineRule="auto" /><w:ind w:firstLine="720" /><w:jc w:val="both" />', ""),
    "FirstParagraph": estilo("FirstParagraph", "First Paragraph", '<w:spacing w:before="0" w:after="240" w:line="360" w:lineRule="auto" /><w:ind w:firstLine="720" /><w:jc w:val="both" />', "", '<w:next w:val="BodyText" />'),
    "Compact": estilo("Compact", "Compact", '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto" /><w:jc w:val="left" />', '<w:sz w:val="22" /><w:szCs w:val="22" />'),
    "Heading1": estilo("Heading1", "heading 1", '<w:keepNext /><w:keepLines /><w:pageBreakBefore /><w:suppressAutoHyphens /><w:spacing w:before="240" w:after="480" w:line="360" w:lineRule="auto" /><w:jc w:val="center" /><w:outlineLvl w:val="0" />',
                       f'{TNR}<w:b /><w:caps /><w:sz w:val="28" /><w:szCs w:val="28" />', '<w:next w:val="BodyText" />'),
    "Heading2": estilo("Heading2", "heading 2", '<w:keepNext /><w:keepLines /><w:suppressAutoHyphens /><w:spacing w:before="360" w:after="240" w:line="360" w:lineRule="auto" /><w:jc w:val="left" /><w:outlineLvl w:val="1" />',
                       f'{TNR}<w:b /><w:sz w:val="24" /><w:szCs w:val="24" />', '<w:next w:val="BodyText" />'),
    "Heading3": estilo("Heading3", "heading 3", '<w:keepNext /><w:keepLines /><w:suppressAutoHyphens /><w:spacing w:before="240" w:after="120" w:line="360" w:lineRule="auto" /><w:jc w:val="left" /><w:outlineLvl w:val="2" />',
                       f'{TNR}<w:b /><w:i /><w:sz w:val="24" /><w:szCs w:val="24" />', '<w:next w:val="BodyText" />'),
    "ImageCaption": estilo("ImageCaption", "Image Caption", '<w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto" /><w:jc w:val="center" />', '<w:sz w:val="20" /><w:szCs w:val="20" />'),
    "TableCaption": estilo("TableCaption", "Table Caption", '<w:keepNext /><w:spacing w:before="120" w:after="60" w:line="240" w:lineRule="auto" /><w:jc w:val="left" />', '<w:b /><w:sz w:val="20" /><w:szCs w:val="20" />'),
    "Caption": estilo("Caption", "caption", '<w:spacing w:before="60" w:after="240" w:line="240" w:lineRule="auto" /><w:jc w:val="center" />', '<w:sz w:val="20" /><w:szCs w:val="20" />'),
    "CaptionedFigure": estilo("CaptionedFigure", "Captioned Figure", '<w:keepNext /><w:spacing w:before="120" w:after="0" /><w:jc w:val="center" />', ""),
    "Figure": estilo("Figure", "Figure", '<w:spacing w:before="120" w:after="0" /><w:jc w:val="center" />', ""),
    "Bibliography": estilo("Bibliography", "Bibliography", '<w:spacing w:after="120" w:line="240" w:lineRule="auto" /><w:ind w:left="720" w:hanging="720" /><w:jc w:val="left" />', ""),
    "Title": estilo("Title", "Title", '<w:suppressAutoHyphens /><w:spacing w:before="0" w:after="160" w:line="240" w:lineRule="auto" /><w:jc w:val="center" />', f'{TNR}<w:b /><w:sz w:val="32" /><w:szCs w:val="32" />'),
    "TOCHeading": estilo("TOCHeading", "TOC Heading", '<w:keepNext /><w:spacing w:before="240" w:after="480" /><w:jc w:val="center" /><w:outlineLvl w:val="9" />', f'{TNR}<w:b /><w:caps /><w:sz w:val="28" /><w:szCs w:val="28" />'),
}

estilos = (base / "word" / "styles.xml").read_text(encoding="utf-8")
estilos = re.sub(r'<w:rFonts w:asciiTheme="minorHAnsi"[^/]*/>', TNR, estilos, count=1)
estilos = estilos.replace('<w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA" />', '<w:lang w:val="es-PE" w:eastAsia="en-US" w:bidi="ar-SA" />')
for sid, xml in nuevos.items():
    patron = re.compile(r'<w:style w:type="paragraph"(?: w:default="1")? w:styleId="%s">.*?</w:style>' % sid, re.S)
    if patron.search(estilos):
        estilos = patron.sub(lambda _m: xml, estilos, count=1)
    else:
        estilos = estilos.replace("</w:styles>", xml + "</w:styles>")
# Hipervínculos y código en negro, sin colores
estilos = re.sub(r'<w:color w:val="[0-9A-F]{6}"[^/]*/>', "", estilos)

# Tablas académicas de tres líneas: borde superior e inferior de la tabla y borde bajo el encabezado
BORDES = ('<w:tblBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="000000" />'
          '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000" /></w:tblBorders>')
estilos = estilos.replace('<w:tblInd w:w="0" w:type="dxa" />', '<w:tblInd w:w="0" w:type="dxa" />' + BORDES, 1)
estilos = estilos.replace('<w:bottom w:val="single"/>', '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>')
assert "tblBorders" in estilos, "no se aplicaron los bordes de tabla"

ajustes = (base / "word" / "settings.xml").read_text(encoding="utf-8")
if "autoHyphenation" not in ajustes:
    ajustes = ajustes.replace('<w:zoom w:percent="100" />', '<w:zoom w:percent="100" /><w:autoHyphenation />', 1)
assert "autoHyphenation" in ajustes

documento = (base / "word" / "document.xml").read_text(encoding="utf-8")
sect = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdPie1" />'
        '<w:footnotePr><w:numRestart w:val="eachSect" /></w:footnotePr>'
        '<w:pgSz w:w="11906" w:h="16838" />'
        '<w:pgMar w:top="1701" w:right="1417" w:bottom="1417" w:left="1701" w:header="709" w:footer="709" w:gutter="0" />'
        '<w:pgNumType w:start="1" /></w:sectPr>')
documento = re.sub(r"<w:sectPr>.*?</w:sectPr>", sect, documento, flags=re.S)

pie = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
       '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
       'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
       '<w:p><w:pPr><w:jc w:val="center" /></w:pPr>'
       f'<w:r><w:rPr>{TNR}<w:sz w:val="24" /></w:rPr><w:fldChar w:fldCharType="begin" /></w:r>'
       f'<w:r><w:rPr>{TNR}<w:sz w:val="24" /></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
       f'<w:r><w:rPr>{TNR}<w:sz w:val="24" /></w:rPr><w:fldChar w:fldCharType="separate" /></w:r>'
       f'<w:r><w:rPr>{TNR}<w:sz w:val="24" /></w:rPr><w:t>1</w:t></w:r>'
       f'<w:r><w:rPr>{TNR}<w:sz w:val="24" /></w:rPr><w:fldChar w:fldCharType="end" /></w:r></w:p></w:ftr>')

rels = (base / "word" / "_rels" / "document.xml.rels").read_text(encoding="utf-8")
if "rIdPie1" not in rels:
    rels = rels.replace("</Relationships>",
                        '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Id="rIdPie1" Target="footer1.xml" /></Relationships>')
tipos = (base / "[Content_Types].xml").read_text(encoding="utf-8")
if "footer1.xml" not in tipos:
    tipos = tipos.replace("</Types>", '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" /></Types>')

with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
    for ruta in base.rglob("*"):
        if ruta.is_dir():
            continue
        nombre = ruta.relative_to(base).as_posix()
        if nombre == "word/styles.xml":
            z.writestr(nombre, estilos)
        elif nombre == "word/document.xml":
            z.writestr(nombre, documento)
        elif nombre == "word/_rels/document.xml.rels":
            z.writestr(nombre, rels)
        elif nombre == "word/settings.xml":
            z.writestr(nombre, ajustes)
        elif nombre == "[Content_Types].xml":
            z.writestr(nombre, tipos)
        else:
            z.write(ruta, nombre)
    z.writestr("word/footer1.xml", pie)
print("ok", salida)
