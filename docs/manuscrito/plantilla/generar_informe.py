"""Genera el informe de Seminario de Tesis (Word y, opcionalmente, PDF) desde los capítulos en Markdown.

Uso (desde la raíz del repositorio):

    python docs/manuscrito/plantilla/generar_informe.py --pandoc RUTA/pandoc.exe \
        --salida docs/manuscrito/MCC702_informe.docx [--pdf]

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
    # Espacio tras cada tabla: el párrafo siguiente (texto o título de cuadro) no queda pegado al borde inferior
    doc = doc.replace("</w:tbl>", '</w:tbl><w:p><w:pPr><w:spacing w:before="0" w:after="120" w:line="240" '
                                  'w:lineRule="auto" /></w:pPr></w:p>')
    partes["word/document.xml"] = doc.encode("utf-8")
    with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as z:
        for nombre, datos in partes.items():
            z.writestr(nombre, datos)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pandoc", required=True)
    parser.add_argument("--salida", required=True)
    parser.add_argument("--pdf", action="store_true")
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
    print(f"Word -> {salida}")
    if args.pdf:
        pdf = salida.with_suffix(".pdf")
        ps = PDF_PS1.format(docx=str(salida), pdf=str(pdf))
        subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps], check=True)
        print(f"PDF -> {pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
