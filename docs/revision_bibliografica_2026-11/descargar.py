"""Descarga los PDF del manifiesto y, con --busquedas, exporta las consultas de OpenAlex.

Uso (desde cualquier carpeta):
    python descargar.py              # PDF -> pdfs/
    python descargar.py --busquedas  # JSON -> busquedas/
Solo biblioteca estandar. No sobrescribe archivos existentes.
"""
import csv, hashlib, json, sys, time, urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
UA = {"User-Agent": "revision-bibliografica-tesis/1.0 (uso academico)"}


def bajar(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
        return r.read()


def pdfs() -> int:
    carpeta = AQUI / "pdfs"
    fallos = 0
    with open(carpeta / "MANIFIESTO.csv", encoding="utf-8", newline="") as f, \
            open(carpeta / "descargas.log", "a", encoding="utf-8") as log:
        for fila in csv.DictReader(f):
            destino = carpeta / fila["archivo"]
            if destino.exists():
                continue
            if not fila["url_pdf"]:
                print(f'{fila["id"]}: {fila["nota"]}')
                continue
            try:
                datos = bajar(fila["url_pdf"])
                if not datos.startswith(b"%PDF"):
                    raise ValueError("la respuesta no es un PDF")
                destino.write_bytes(datos)
                log.write(f'{fila["id"]}\t{hashlib.sha256(datos).hexdigest()}\t{fila["url_pdf"]}\n')
                print(f'{fila["id"]}: ok ({len(datos) // 1024} kB)')
            except Exception as e:  # se informa y se sigue con el resto
                fallos += 1
                log.write(f'{fila["id"]}\tFALLO {e}\t{fila["url_pdf"]}\n')
                print(f'{fila["id"]}: FALLO ({e}) -> bajar a mano: {fila["url_pdf"]}')
            time.sleep(3)
    return fallos


def busquedas() -> int:
    carpeta = AQUI / "busquedas"
    consultas = json.loads((carpeta / "consultas_openalex.json").read_text(encoding="utf-8"))
    fallos = 0
    for clave, c in consultas.items():
        try:
            (carpeta / f"openalex_{clave}.json").write_bytes(bajar(c["url"]))
            print(f"{clave}: ok")
        except Exception as e:
            fallos += 1
            print(f"{clave}: FALLO ({e})")
        time.sleep(2)
    return fallos


if __name__ == "__main__":
    sys.exit(1 if (busquedas() if "--busquedas" in sys.argv else pdfs()) else 0)
