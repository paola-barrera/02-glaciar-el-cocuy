# %% Conectar con Google Earth Engine y cargar la configuración
import ee
import geemap
import pandas as pd
from a_config import PROYECTO_GEE, AREA_COORDS

ee.Initialize(project=PROYECTO_GEE)
area = ee.Geometry.Rectangle(AREA_COORDS)

ANO = 2026

inicio = ee.Date.fromYMD(ANO - 1, 12, 1)
fin = ee.Date.fromYMD(ANO, 3, 1)

# Satélite: (colección, bandas color natural, bandas falso color)
SENSORES = {
    "L7": ("LANDSAT/LE07/C02/T1_L2", ["SR_B3", "SR_B2", "SR_B1"], ["SR_B5", "SR_B4", "SR_B3"]),
    "L8": ("LANDSAT/LC08/C02/T1_L2", ["SR_B4", "SR_B3", "SR_B2"], ["SR_B6", "SR_B5", "SR_B4"]),
    "L9": ("LANDSAT/LC09/C02/T1_L2", ["SR_B4", "SR_B3", "SR_B2"], ["SR_B6", "SR_B5", "SR_B4"]),
}
#%%
coleccion = ee.ImageCollection([])
for _, (id_coleccion, _, _) in SENSORES.items():
    coleccion = coleccion.merge(ee.ImageCollection(id_coleccion))

coleccion = (
    coleccion
    .filterBounds(area)
    .filterDate(inicio, fin)
)

propiedades = ["SPACECRAFT_ID", "DATE_ACQUIRED", "WRS_PATH", "WRS_ROW", "CLOUD_COVER"]

datos = (
    coleccion
    .reduceColumns(ee.Reducer.toList(len(propiedades)), propiedades)
    .get("list")
    .getInfo()
)

tabla_colecciones = pd.DataFrame(datos, columns=["satelite", "fecha", "path", "fila", "nubes_escena_%"])
tabla_colecciones = tabla_colecciones.sort_values(["satelite", "nubes_escena_%"])
tabla_colecciones

# %% Ver una imagen concreta
SATELITE = "LANDSAT_8"   # L5, L7, L8, L9
FECHA = "2026-02-12"
FILA = 56

imagen = (
    coleccion
    .filter(ee.Filter.eq("SPACECRAFT_ID", SATELITE))
    .filter(ee.Filter.eq("DATE_ACQUIRED", FECHA))
    .filter(ee.Filter.eq("WRS_ROW", FILA))
    .first() 
)
reflectancia = imagen.select("SR_B.").multiply(0.0000275).add(-0.2).clip(area)

# Las bandas cambian según el satélite
if SATELITE in ["LANDSAT_5", "LANDSAT_7"]:
    vis_natural = {"bands": ["SR_B3", "SR_B2", "SR_B1"], "min": 0, "max": 0.4}
    vis_falso_color = {"bands": ["SR_B5", "SR_B4", "SR_B3"], "min": 0, "max": 0.4}
else:  # Landsat 8 y 9
    vis_natural = {"bands": ["SR_B4", "SR_B3", "SR_B2"], "min": 0, "max": 0.4}
    vis_falso_color = {"bands": ["SR_B6", "SR_B5", "SR_B4"], "min": 0, "max": 0.4}

Map = geemap.Map()
Map.centerObject(area, zoom=12)
Map.add_basemap("SATELLITE")
Map.addLayer(reflectancia, vis_natural, f"{SATELITE} {FECHA} fila {FILA} natural")
Map.addLayer(reflectancia, vis_falso_color, f"{SATELITE} {FECHA} fila {FILA} falso")
Map

# %%
