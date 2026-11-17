# %% Librerías y configuración
from pathlib import Path

import pandas as pd
import rasterio
from a_config import TEMPORADAS, AREA_IDEAM
import numpy as np

CARPETA_OUTPUT = Path("../outputs")

# %% Área de nieve de cada temporada
filas = []
for ano in TEMPORADAS:
    with rasterio.open(CARPETA_OUTPUT / f"{ano}_nieve.tif") as archivo:
        nieve = archivo.read(1) #lee la primera banda, aunque nieve solo tiene una
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

# %% Altitud de la nieve y el hielo en cada temporada
with rasterio.open(CARPETA_OUTPUT / "dem.tif") as archivo:
    dem = archivo.read(1)
    transform_dem = archivo.transform

filas_altitud = []
for ano in TEMPORADAS:
    with rasterio.open(CARPETA_OUTPUT / f"{ano}_nieve.tif") as archivo:
        nieve = archivo.read(1)
        transform_nieve = archivo.transform
        

    if nieve.shape != dem.shape or transform_nieve != transform_dem:
        raise ValueError(f"El DEM y la máscara de {ano} no tienen la misma rejilla")
        

    altitudes = dem[nieve == 1]

    filas_altitud.append({
        "temporada": ano,
        "altitud_min_m": round(float(altitudes.min())),
        "altitud_p5_m": round(float(np.percentile(altitudes, 5))),
        "altitud_mediana_m": round(float(np.median(altitudes))),
        "altitud_max_m": round(float(altitudes.max())),
    })

tabla_altitud = pd.DataFrame(filas_altitud)
tabla_altitud