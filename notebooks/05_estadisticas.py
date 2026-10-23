# %% Librerías y configuración
from pathlib import Path

import pandas as pd
import rasterio
from a_config import TEMPORADAS, AREA_IDEAM

CARPETA_OUTPUT = Path("../data/output")

# %% Área de nieve de cada temporada
filas = []
for ano in TEMPORADAS:
    with rasterio.open(CARPETA_OUTPUT / f"{ano}_nieve.tif") as archivo:
        nieve = archivo.read(1) #lee la primera banda
        ancho_px, alto_px = archivo.res

    area_pixel_m2 = ancho_px * alto_px
    n_pixeles = int((nieve == 1).sum())
    area_km2 = n_pixeles * area_pixel_m2 / 1e6

    filas.append({
        "temporada": ano,
        "pixeles_nieve": n_pixeles,
        "area_km2": round(area_km2, 2),
        "ideam_km2": AREA_IDEAM.get(ano),
    })

tabla_areas = pd.DataFrame(filas)
tabla_areas