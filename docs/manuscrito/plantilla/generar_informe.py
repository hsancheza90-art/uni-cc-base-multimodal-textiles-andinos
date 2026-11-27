"""Genera el informe de Seminario de Tesis (Word y, opcionalmente, PDF) desde los capítulos en Markdown.

Uso (desde la raíz del repositorio):

    python docs/manuscrito/plantilla/generar_informe.py --pandoc RUTA/pandoc.exe \
        --salida docs/manuscrito/MCC702_informe.docx [--pdf] [--firmas docs/manuscrito/firmas]

Pasos: 1) plantilla de Word con el formato de la guía UNI (hacer_referencia.py); 2) pandoc con citeproc y
estilo IEEE, el filtro que conserva el número de las ecuaciones (tag.lua) y la portada e índice de esta carpeta;
3) ajuste de la paginación: romanos en los preliminares (portada sin número) y arábigos desde el capítulo 1;
4) con --pdf, Word actualiza el índice y los campos y exporta a PDF (requiere Word instalado).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

PLANTILLA = Path(__file__).resolve().parent
MANUSCRITO = PLANTILLA.parent

ORDEN = [
    PLANTILLA / "portada.md",
    MANUSCRITO / "00_resumen.md",
    PLANTILLA / "indice.md",
    *[MANUSCRITO / f"capitulo_{n}_{s}.md" for n, s in [
        (1, "introduccion"), (2, "problema_objetivos_hipotesis"), (3, "estado_del_arte"),
        (4, "datos_y_anotacion"), (5, "metodo_formal"), (6, "implementacion"),
        (7, "diseno_experimental"), (8, "resultados"), (9, "discusion"), (10, "conclusiones"),
        (11, "limitaciones_trabajo_futuro")]],
    PLANTILLA / "referencias.md",
    MANUSCRITO / "anexo_A_implementacion.md",
    MANUSCRITO / "anexo_B_custodia_y_decisiones.md",
    MANUSCRITO / "anexo_C_primer_avance.md",
]

PDF_PS1 = r"""
$docx = '{docx}'; $pdf = '{pdf}'
$w = New-Object -ComObject Word.Application; $w.Visible = $false; $w.DisplayAlerts = 0
try {{
  $d = $w.Documents.Open($docx)
  foreach ($t in $d.TablesOfContents) {{ $t.Update() }}
  $d.Fields.Update() | Out-Null
  foreach ($t in $d.TablesOfContents) {{ $t.UpdatePageNumbers() }}
  $d.Save()
  $d.ExportAsFixedFormat($pdf, 17)
  $d.Close()
}} finally {{ $w.Quit() }}
"""


ANCHO_TEXTO = 8788       # ancho de la caja de texto en twips (A4 con márgenes de 30 y 25 mm)
TWIPS_POR_CARACTER = 115  # aproximación conservadora para Times New Roman de 12 pt
FILAS_CUADRO_CORTO = 15   # los cuadros cortos (hasta estas filas y estos caracteres) no se parten entre páginas;
CARACTERES_CUADRO_CORTO = 700  # los largos sí, entre filas y con el encabezado repetido
NBSP, ZWSP, NDASH, WJ = " ", "​", "–", "⁠"


def _cortes(doc: str) -> str:
    """Cortes de línea: «p. N», cifra y «%» sin separar; rangos de páginas con raya corta;
    el código solo se corta tras «_», «/» o «.»."""
    def texto(m: re.Match) -> str:
        t = m.group(2)
        t = re.sub(r"\b(pp?\.) (?=[0-9{])", r"\1" + NBSP, t)
        t = re.sub(r"([0-9]) %", r"\1" + NBSP + "%", t)
        t = re.sub(r"(pp\." + NBSP + r"[0-9]+)-([0-9]+)", r"\1" + NDASH + WJ + r"\2", t)
        return m.group(1) + t + m.group(3)
    doc = re.sub(r"(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)", texto, doc)

    def codigo(m: re.Match) -> str:
        return m.group(1) + re.sub(r"([_/.])(?=[^\s])", r"\1" + ZWSP, m.group(2)) + m.group(3)
    return re.sub(r'(<w:rStyle w:val="VerbatimChar" /></w:rPr><w:t(?: [^>]*)?>)([^<]*)(</w:t>)', codigo, doc)


def _texto(xml: str) -> str:
    return "".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", xml))


def _anchos(filas: list[list[str]]) -> list[int] | None:
    """Ancho de cada columna según su contenido: ninguna palabra partida si cabe, el resto por longitud media."""
    ncol = len(filas[0])
    if any(len(f) != ncol for f in filas):
        return None
    capacidad = ANCHO_TEXTO / TWIPS_POR_CARACTER
    margen = 3.0  # márgenes internos de la celda, en caracteres
    # Palabra más larga que no puede cortarse (el código se corta tras «_», «/», «.» o «-»), con holgura
    tramos = lambda s: re.split(r"[\s_/.\-]+", s)
    palabra = [min(16, max((len(p) for f in filas for p in tramos(f[j])), default=1)) * 1.15 + margen + 1
               for j in range(ncol)]
    maximo = [max(len(f[j]) for f in filas) + margen for j in range(ncol)]
    minimo = [min(palabra[j], maximo[j]) for j in range(ncol)]
    if sum(maximo) <= capacidad:  # todo cabe en una línea: proporcional a lo más largo
        pesos = maximo
    elif sum(minimo) >= capacidad:
        pesos = minimo
    else:
        # Reparto proporcional a la celda más larga, sin bajar de la palabra más larga de cada columna
        fijas: dict[int, float] = {}
        while True:
            libres = [j for j in range(ncol) if j not in fijas]
            escala = (capacidad - sum(fijas.values())) / sum(maximo[j] for j in libres)
            nuevas = {j: minimo[j] for j in libres if maximo[j] * escala < minimo[j]}
            if not nuevas:
                break
            fijas.update(nuevas)
        pesos = [fijas.get(j, maximo[j] * escala) for j in range(ncol)]
    suma = sum(pesos)
    anchos = [int(ANCHO_TEXTO * p / suma) for p in pesos]
    anchos[-1] += ANCHO_TEXTO - sum(anchos)
    return anchos


def _cuadro(tbl: str) -> str:
    """Filas que no se parten, cuadros cortos sin partir y anchos de columna según el contenido."""
    if 'w:tblStyle w:val="Table"' not in tbl or "<w:tbl>" in tbl[7:]:
        return tbl
    filas = re.findall(r"<w:tr>.*?</w:tr>", tbl, flags=re.S)
    corto = len(filas) <= FILAS_CUADRO_CORTO and len(_texto(tbl)) <= CARACTERES_CUADRO_CORTO
    nuevas = []
    for k, fila in enumerate(filas):
        if "<w:trPr>" in fila:
            fila = fila.replace("<w:trPr>", "<w:trPr><w:cantSplit />", 1)
        else:
            fila = fila.replace("<w:tr>", "<w:tr><w:trPr><w:cantSplit /></w:trPr>", 1)
        if corto and k < len(filas) - 1:
            fila = fila.replace('<w:pStyle w:val="Compact" />', '<w:pStyle w:val="Compact" /><w:keepNext />')
        nuevas.append(fila)
    for vieja, nueva in zip(filas, nuevas):
        tbl = tbl.replace(vieja, nueva, 1)
    if "gridSpan" in tbl:
        return tbl
    celdas = [[_texto(c) for c in re.findall(r"<w:tc>.*?</w:tc>", f, flags=re.S)] for f in nuevas]
    if any("Promedio del jurado" in c for f in celdas for c in f):  # portada: espacio para escribir y firmar
        anchos = [3000, 2988, 1000, 1800]
    else:
        anchos = _anchos(celdas) if celdas and celdas[0] else None
    if not anchos or tbl.count("<w:gridCol ") != len(anchos):
        return tbl
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{a}" />' for a in anchos) + "</w:tblGrid>"
    tbl = re.sub(r"<w:tblGrid>.*?</w:tblGrid>", grid, tbl, count=1, flags=re.S)

    def ancho_celdas(m: re.Match) -> str:
        fila, j = m.group(0), iter(anchos)
        return re.sub(r"<w:tcPr />|<w:tcPr>", lambda c: (f'<w:tcPr><w:tcW w:w="{next(j)}" w:type="dxa" />'
                                                        + ("</w:tcPr>" if c.group(0) == "<w:tcPr />" else "")), fila)
    return re.sub(r"<w:tr>.*?</w:tr>", ancho_celdas, tbl, flags=re.S)


def maquetar(doc: str) -> str:
    """Ajustes de maquetación que pandoc no expresa: títulos de cuadro, cuadros, listas y leyendas."""
    # Título de cuadro («**Cuadro X.Y.** …»): unido al cuadro, sin sangría ni partición silábica
    doc = re.sub(r'<w:pPr><w:pStyle w:val="(BodyText|FirstParagraph)" /></w:pPr>'
                 r'(<w:r><w:rPr><w:b /><w:bCs /></w:rPr><w:t xml:space="preserve">Cuadro [A-Z0-9]+\.[0-9]+\.</w:t>)',
                 r'<w:pPr><w:pStyle w:val="\1" /><w:keepNext /><w:keepLines /><w:suppressAutoHyphens />'
                 r'<w:spacing w:before="120" w:after="60" /><w:ind w:firstLine="0" /><w:jc w:val="left" /></w:pPr>\2', doc)
    doc = re.sub(r"<w:tbl>.*?</w:tbl>", lambda m: _cuadro(m.group(0)), doc, flags=re.S)
    # Rótulo de figura en negrita, como el de los cuadros
    doc = re.sub(r'(<w:pStyle w:val="ImageCaption" /></w:pPr>)<w:r><w:t xml:space="preserve">(Figura [A-Z0-9]+\.[0-9]+\.)',
                 r'\1<w:r><w:rPr><w:b /><w:bCs /></w:rPr><w:t xml:space="preserve">\2</w:t></w:r>'
                 r'<w:r><w:t xml:space="preserve">', doc)
    # Espacio después del último elemento de cada lista
    parrafos = list(re.finditer(r"<w:p>.*?</w:p>", doc, flags=re.S))
    cambios = []
    for actual, siguiente in zip(parrafos, parrafos[1:]):
        if ("<w:numPr>" in actual.group(0) and "<w:numPr>" not in siguiente.group(0)
                and not doc[actual.end():siguiente.start()].strip()):
            cambios.append(actual)
    for m in reversed(cambios):
        p = m.group(0).replace("</w:pPr>", '<w:spacing w:after="240" /></w:pPr>', 1)
        doc = doc[:m.start()] + p + doc[m.end():]
    # Texto que continúa la frase después de una ecuación numerada: sin sangría de primera línea
    doc = re.sub(r'(<w:pStyle w:val="Ecuacion" />(?:(?!</w:p>).)*</w:p>\s*<w:p><w:pPr><w:pStyle w:val="(?:BodyText|FirstParagraph)" />)'
                 r'(</w:pPr><w:r>(?:<w:rPr>.*?</w:rPr>)?<w:t(?: [^>]*)?>[a-záéíóúñ])',
                 r'\1<w:ind w:firstLine="0" />\2', doc, flags=re.S)
    return _cortes(doc)


def paginacion(docx: Path) -> None:
    """Romanos con portada sin número en la sección de preliminares; arábigos desde 1 en el cuerpo."""
    with zipfile.ZipFile(docx) as z:
        partes = {n: z.read(n) for n in z.namelist()}
    doc = partes["word/document.xml"].decode("utf-8")
    secciones = re.findall(r"<w:sectPr\b.*?</w:sectPr>", doc, flags=re.S)
    final = secciones[-1]
    pie = re.search(r'<w:footerReference [^>]*/>', final)
    if not pie:
        raise SystemExit("La última sección no tiene pie de página: revise la plantilla.")
    romana = next((s for s in secciones if 'w:fmt="lowerRoman"' in s), None)
    if romana is None:
        raise SystemExit("No se encontró la sección de preliminares (indice.md).")
    doc = doc.replace(romana, romana.replace("<w:sectPr>", "<w:sectPr>" + pie.group(0), 1), 1)
    nueva_final = re.sub(r"<w:pgNumType[^>]*/>", '<w:pgNumType w:fmt="decimal" w:start="1" />', final)
    doc = doc[: doc.rindex(final)] + nueva_final + doc[doc.rindex(final) + len(final):]
    doc = maquetar(doc)
    # Espacio tras cada tabla: el párrafo siguiente (texto o título de cuadro) no queda pegado al borde inferior
    doc = doc.replace("</w:tbl>", '</w:tbl><w:p><w:pPr><w:spacing w:before="0" w:after="120" w:line="240" '
                                  'w:lineRule="auto" /></w:pPr></w:p>')
    partes["word/document.xml"] = doc.encode("utf-8")
    with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as z:
        for nombre, datos in partes.items():
            z.writestr(nombre, datos)


# Marcas de la portada y archivo de cada firma dentro de la carpeta --firmas (no versionada).
FIRMAS = {"FIRMA_ASESOR": "firma_lara.jpg", "FIRMA_TESISTA": "firma_henry.jpg"}
FIRMA_MAX_CM = (4.5, 1.6)  # ancho y alto máximos de la imagen de una firma
EMU_CM = 360000

DIBUJO = (
    '<w:r><w:drawing><wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{id}" name="{nombre}"/>'
    '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
    '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<pic:nvPicPr><pic:cNvPr id="0" name="{nombre}"/><pic:cNvPicPr/></pic:nvPicPr>'
    '<pic:blipFill><a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{rid}"/>'
    '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
    '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
    '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')


def firmas(docx: Path, carpeta: Path | None) -> None:
    """Sustituye las marcas de firma de la portada por las imágenes de `carpeta`, o las borra si no se indica."""
    with zipfile.ZipFile(docx) as z:
        partes = {n: z.read(n) for n in z.namelist()}
    doc = partes["word/document.xml"].decode("utf-8")
    rels = partes["word/_rels/document.xml.rels"].decode("utf-8")
    tipos = partes["[Content_Types].xml"].decode("utf-8")
    for n, (marca, archivo) in enumerate(FIRMAS.items(), start=1):
        corrida = f"<w:r><w:t>{marca}</w:t></w:r>"
        if corrida not in doc:
            raise SystemExit(f"La portada no tiene la marca {marca}.")
        if carpeta is None:
            doc = doc.replace(corrida, "")
            continue
        ruta = carpeta / archivo
        if not ruta.exists():
            raise SystemExit(f"No existe la firma {ruta}.")
        from PIL import Image  # solo se necesita al incrustar firmas
        ancho, alto = Image.open(ruta).size
        escala = min(FIRMA_MAX_CM[0] / ancho, FIRMA_MAX_CM[1] / alto)
        cx, cy = round(ancho * escala * EMU_CM), round(alto * escala * EMU_CM)
        rid, medio = f"rIdFirma{n}", f"media/firma_{n}{ruta.suffix.lower()}"
        partes[f"word/{medio}"] = ruta.read_bytes()
        rels = rels.replace("</Relationships>", f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                            f'officeDocument/2006/relationships/image" Target="{medio}"/></Relationships>')
        extension = ruta.suffix.lower().lstrip(".")
        if f'Extension="{extension}"' not in tipos:
            mime = "image/jpeg" if extension in ("jpg", "jpeg") else f"image/{extension}"
            tipos = tipos.replace("<Default ", f'<Default Extension="{extension}" ContentType="{mime}"/><Default ', 1)
        doc = doc.replace(corrida, DIBUJO.format(cx=cx, cy=cy, id=9000 + n, nombre=f"Firma {n}", rid=rid))
    partes["word/document.xml"] = doc.encode("utf-8")
    partes["word/_rels/document.xml.rels"] = rels.encode("utf-8")
    partes["[Content_Types].xml"] = tipos.encode("utf-8")
    with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as z:
        for nombre, datos in partes.items():
            z.writestr(nombre, datos)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pandoc", required=True)
    parser.add_argument("--salida", required=True)
    parser.add_argument("--pdf", action="store_true")
    parser.add_argument("--firmas", help="Carpeta con las imágenes de las firmas (no se versiona); sin ella, "
                                         "la portada queda con las líneas de firma en blanco.")
    parser.add_argument("--sin-citas", action="store_true", help="Sin citeproc (solo para probar el formato).")
    args = parser.parse_args(argv)
    salida = Path(args.salida).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        referencia = Path(tmp) / "referencia_uni.docx"
        subprocess.run([sys.executable, str(PLANTILLA / "hacer_referencia.py"), str(PLANTILLA / "base"), str(referencia)], check=True)
        orden = [str(p) for p in ORDEN]
        cmd = [args.pandoc, *orden, "-f", "markdown+tex_math_dollars-auto_identifiers",
               "--reference-doc", str(referencia), "--resource-path", str(MANUSCRITO),
               "--lua-filter", str(PLANTILLA / "tag.lua"),
               "-M", "lang=es-PE", "-o", str(salida)]
        if not args.sin_citas:
            cmd[-2:-2] = ["--citeproc", "--bibliography", str(MANUSCRITO / "referencias.bib"),
                          "--csl", str(PLANTILLA / "ieee.csl"), "-M", "link-citations=true"]
        resultado = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if resultado.stderr.strip():
            print(resultado.stderr)
        if resultado.returncode:
            return resultado.returncode
    paginacion(salida)
    firmas(salida, Path(args.firmas).resolve() if args.firmas else None)
    print(f"Word -> {salida}")
    if args.pdf:
        pdf = salida.with_suffix(".pdf")
        ps = PDF_PS1.format(docx=str(salida), pdf=str(pdf))
        subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps], check=True)
        print(f"PDF -> {pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
