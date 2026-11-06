"""M2: embeddings de imagen con OpenCLIP congelado (fuera del flujo: necesita torch e imágenes locales).

Uso desde la raíz del repositorio (con las dependencias de requirements-modelos.txt):

    python -m src.modelos.m2_openclip
    python -m src.modelos.m2_openclip --dispositivo cpu

Lee las copias de evaluación del manifiesto (data/metadata/imagenes_evaluacion_manifiesto_v2.csv,
las descargadas con estado ok), verifica el SHA-256 de cada una y calcula su embedding con el
checkpoint de [m2] en config/modelos.toml, sin ajuste de ningún tipo. Escribe, como insumos
versionados que el flujo solo lee:

- data/metadata/m2_openclip_embeddings_v2.npy: matriz float32 (imágenes × dimensión), filas de
  norma 1, redondeadas a 6 decimales.
- data/metadata/m2_openclip_indice_v2.csv: id_global, fuente y SHA-256 de la copia de cada fila.
- data/metadata/m2_openclip_manifiesto_v2.json: checkpoint, SHA-256 del archivo de pesos,
  versiones, dispositivo, encuadre y hashes de las salidas.
- outputs/reports/m2_openclip_v2.md: lo anterior y las comprobaciones (normas, determinismo
  entre dos pasadas y entre GPU y CPU).

Encuadre: con "relleno_cuadrado" la imagen se lleva a un cuadrado con el color mediano de su
borde antes del preprocesamiento del modelo, para que el recorte central no corte los extremos
de las piezas alargadas. No muestra rankings: la galería del protocolo se juzga a ciegas.
"""

from __future__ import annotations

import argparse
import platform
import sys
import time
from importlib import metadata
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from src.imagenes.descargar_evaluacion import imagenes_verificadas, sha256_archivo
from src.modelos.embeddings import (
    COLUMNAS_INDICE,
    EMBEDDINGS_M2,
    INDICE_M2,
    MANIFIESTO_M2,
    normalizar_l2,
    redondear,
)
from src.utils.archivos import escribir_csv, escribir_json, escribir_texto
from src.utils.config import CONFIG_MODELOS, leer_config_modelos

REPORTE_M2 = "outputs/reports/m2_openclip_v2.md"
PAQUETES = ["torch", "torchvision", "open_clip_torch", "transformers", "huggingface_hub", "numpy", "Pillow"]


def relleno_cuadrado(imagen: Image.Image) -> Image.Image:
    """Cuadrado de lado max(ancho, alto) con el color mediano del borde y la imagen centrada."""
    imagen = imagen.convert("RGB")
    ancho, alto = imagen.size
    if ancho == alto:
        return imagen
    pixeles = np.asarray(imagen)
    borde = np.concatenate([pixeles[0], pixeles[-1], pixeles[:, 0], pixeles[:, -1]])
    color = tuple(int(c) for c in np.median(borde, axis=0))
    lado = max(ancho, alto)
    cuadrado = Image.new("RGB", (lado, lado), color)
    cuadrado.paste(imagen, ((lado - ancho) // 2, (lado - alto) // 2))
    return cuadrado


# --------------------------------------------------------------------------- modelo (torch)


def cargar_modelo(config: dict[str, Any], dispositivo: str):
    import open_clip
    import torch

    torch.manual_seed(0)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    modelo, _, preprocesar = open_clip.create_model_and_transforms(
        config["arquitectura"], pretrained=config["pesos"], device=dispositivo, precision=config["precision"]
    )
    modelo.eval()
    return modelo, preprocesar


def calcular(modelo, preprocesar, rutas: list[Path], encuadre: str, lote: int, dispositivo: str) -> np.ndarray:
    import torch

    bloques = []
    with torch.no_grad():
        for inicio in range(0, len(rutas), lote):
            imagenes = []
            for ruta in rutas[inicio:inicio + lote]:
                with Image.open(ruta) as imagen:
                    imagen = relleno_cuadrado(imagen) if encuadre == "relleno_cuadrado" else imagen.convert("RGB")
                    imagenes.append(preprocesar(imagen))
            tensor = torch.stack(imagenes).to(dispositivo)
            bloques.append(modelo.encode_image(tensor).float().cpu().numpy())
    return normalizar_l2(np.concatenate(bloques).astype(np.float64)).astype(np.float32)


def archivo_pesos(config: dict[str, Any]) -> tuple[str, str, str]:
    """Nombre, revisión y SHA-256 del archivo de pesos en la caché de Hugging Face."""
    from huggingface_hub import snapshot_download

    carpeta = Path(snapshot_download(config["repositorio_pesos"], local_files_only=True,
                                     allow_patterns=["*.bin", "*.safetensors"]))
    archivos = sorted(p for p in carpeta.iterdir() if p.suffix in {".bin", ".safetensors"} and "open_clip" in p.name)
    if len(archivos) != 1:
        raise ValueError(f"Se esperaba un archivo de pesos open_clip en {carpeta}: {[p.name for p in archivos]}")
    return archivos[0].name, carpeta.name, sha256_archivo(archivos[0])


def version(paquete: str) -> str:
    try:
        return metadata.version(paquete)
    except metadata.PackageNotFoundError:
        return ""


def nombre_dispositivo(dispositivo: str) -> str:
    import torch

    if dispositivo.startswith("cuda"):
        return f"{torch.cuda.get_device_name(0)} (CUDA {torch.version.cuda})"
    return platform.processor() or platform.machine()


# --------------------------------------------------------------------------- informe


def lineas_reporte(manifiesto: dict[str, Any], comprobaciones: list[tuple[str, str, str]]) -> list[str]:
    m = manifiesto
    lineas = [
        "# M2: embeddings OpenCLIP (v2)",
        "",
        "Generado por `python -m src.modelos.m2_openclip` (`src/modelos/m2_openclip.py`), fuera del flujo: necesita "
        f"torch y las copias de evaluacion locales. Parametros en `{CONFIG_MODELOS.as_posix()}` ([m2]); protocolo en "
        "`docs/protocolo_experimental_v2.md` (seccion 4). Sistema congelado: sin ajuste ni entrenamiento.",
        "",
        "## Checkpoint",
        "",
        f"- Arquitectura: `{m['arquitectura']}`; pesos: `{m['pesos']}` (`{m['repositorio_pesos']}`, revision "
        f"`{m['revision_pesos']}`).",
        f"- Archivo de pesos: `{m['archivo_pesos']}`, SHA-256 `{m['sha256_pesos']}`. Licencia: {m['licencia_pesos']}.",
        f"- Precision: {m['precision']}; lote: {m['lote']}; encuadre: `{m['encuadre']}`; dispositivo: {m['dispositivo']}.",
        f"- Versiones: " + ", ".join(f"{p} {v}" for p, v in m["versiones"].items() if v) + ".",
        "",
        "## Salidas",
        "",
        f"- `{EMBEDDINGS_M2.as_posix()}`: {m['imagenes']} imagenes x {m['dimension']} dimensiones, float32, filas de "
        f"norma 1 redondeadas a 6 decimales. SHA-256 `{m['sha256_embeddings']}`.",
        f"- `{INDICE_M2.as_posix()}`: id_global, fuente y SHA-256 de la copia de cada fila. SHA-256 `{m['sha256_indice']}`.",
        f"- `{MANIFIESTO_M2.as_posix()}`: este registro en JSON.",
        "",
        "## Comprobaciones",
        "",
        "| Comprobacion | Resultado | Cumple |",
        "|---|---|---|",
    ]
    lineas += [f"| {nombre} | {resultado} | {cumple} |" for nombre, resultado, cumple in comprobaciones]
    lineas += [
        "",
        "El informe no muestra rankings ni vecinos: la galeria del protocolo (el nucleo) se juzga a ciegas. Los "
        "embeddings tambien proponen candidatos a duplicado para los grupos v2 (`outputs/reports/grupos_v2.md`).",
    ]
    return lineas


# --------------------------------------------------------------------------- principal


def ejecutar(raiz: Path, dispositivo: str | None) -> int:
    import torch

    config = leer_config_modelos(raiz)["m2"]
    dispositivo = dispositivo or config["dispositivo"]
    if dispositivo.startswith("cuda") and not torch.cuda.is_available():
        print("CUDA no esta disponible; use --dispositivo cpu.")
        return 1
    filas, errores = imagenes_verificadas(raiz)
    if errores:
        print(f"{len(errores)} copias sin verificar; no se calculan embeddings:")
        for error in errores[:20]:
            print(f"- {error}")
        return 1
    rutas = [raiz / f["ruta_copia_evaluacion"] for f in filas]

    inicio = time.perf_counter()
    modelo, preprocesar = cargar_modelo(config, dispositivo)
    matriz = calcular(modelo, preprocesar, rutas, config["encuadre"], int(config["lote"]), dispositivo)
    segundos = time.perf_counter() - inicio

    muestra = rutas[:int(config["muestra_determinismo"])]
    repeticion = calcular(modelo, preprocesar, muestra, config["encuadre"], int(config["lote"]), dispositivo)
    dif_pasadas = float(np.max(np.abs(repeticion - matriz[:len(muestra)])))
    comprobaciones = []
    normas = np.linalg.norm(redondear(matriz).astype(np.float64), axis=1)
    comprobaciones.append(("Normas de las filas guardadas", f"{normas.min():.6f} a {normas.max():.6f}",
                           "si" if np.allclose(normas, 1, atol=1e-5) else "no"))
    tolerancia = float(config["tolerancia_determinismo"])
    comprobaciones.append((f"Determinismo: dos pasadas sobre {len(muestra)} imagenes, diferencia maxima",
                           f"{dif_pasadas:.1e} (tolerancia {tolerancia:.0e})", "si" if dif_pasadas <= tolerancia else "no"))
    if dispositivo != "cpu":
        modelo_cpu, preprocesar_cpu = cargar_modelo(config, "cpu")
        en_cpu = calcular(modelo_cpu, preprocesar_cpu, muestra, config["encuadre"], int(config["lote"]), "cpu")
        dif_cpu = float(np.max(np.abs(en_cpu - matriz[:len(muestra)])))
        tolerancia_cpu = float(config["tolerancia_dispositivo"])
        comprobaciones.append((f"GPU frente a CPU sobre {len(muestra)} imagenes, diferencia maxima",
                               f"{dif_cpu:.1e} (tolerancia {tolerancia_cpu:.0e})", "si" if dif_cpu <= tolerancia_cpu else "no"))

    guardada = redondear(matriz)
    (raiz / EMBEDDINGS_M2).parent.mkdir(parents=True, exist_ok=True)
    np.save(raiz / EMBEDDINGS_M2, guardada, allow_pickle=False)
    escribir_csv(raiz / INDICE_M2, COLUMNAS_INDICE, [
        {"fila": str(i), "id_global": f["id_global"], "fuente": f["fuente"], "sha256_copia": f["sha256_copia"]}
        for i, f in enumerate(filas)
    ])
    archivo, revision, sha_pesos = archivo_pesos(config)
    manifiesto = {
        "sistema": "M2",
        "arquitectura": config["arquitectura"],
        "pesos": config["pesos"],
        "repositorio_pesos": config["repositorio_pesos"],
        "revision_pesos": revision,
        "archivo_pesos": archivo,
        "sha256_pesos": sha_pesos,
        "licencia_pesos": config["licencia_pesos"],
        "precision": config["precision"],
        "lote": int(config["lote"]),
        "encuadre": config["encuadre"],
        "dispositivo": nombre_dispositivo(dispositivo),
        "versiones": {"python": platform.python_version(), **{p: version(p) for p in PAQUETES}},
        "imagenes": int(guardada.shape[0]),
        "dimension": int(guardada.shape[1]),
        "sha256_embeddings": sha256_archivo(raiz / EMBEDDINGS_M2),
        "sha256_indice": sha256_archivo(raiz / INDICE_M2),
    }
    escribir_json(raiz / MANIFIESTO_M2, manifiesto)
    escribir_texto(raiz / REPORTE_M2, lineas_reporte(manifiesto, comprobaciones))

    print(f"M2: {guardada.shape[0]} embeddings de dimension {guardada.shape[1]} en {segundos:.1f} s ({dispositivo})")
    for nombre, resultado, cumple in comprobaciones:
        print(f"- {nombre}: {resultado} -> {cumple}")
    print(f"Informe: {raiz / REPORTE_M2}")
    return 0 if all(cumple == "si" for _, _, cumple in comprobaciones) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="M2: embeddings de imagen con OpenCLIP congelado.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--dispositivo", default=None, help="cuda o cpu (por defecto, [m2] dispositivo).")
    args = parser.parse_args(argv)
    return ejecutar(Path(args.root).resolve(), args.dispositivo)


if __name__ == "__main__":
    sys.exit(main())
