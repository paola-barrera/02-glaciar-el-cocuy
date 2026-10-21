# %% Conectar con Google Earth Engine y cargar la configuración
import ee
import geemap
from a_config import PROYECTO_GEE, AREA_COORDS, FECHAS_DESPEJADAS, TEMPORADAS

ee.Initialize(project=PROYECTO_GEE)
area = ee.Geometry.Rectangle(AREA_COORDS)

# %% Bandas de cada colección, en orden: azul, verde, rojo, NIR, SWIR1, SWIR2
BANDAS = {
    "LANDSAT/LT05/C02/T1_L2": ["SR_B1", "SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B7"],
    "LANDSAT/LE07/C02/T1_L2": ["SR_B1", "SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B7"],
    "LANDSAT/LC08/C02/T1_L2": ["SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B6", "SR_B7"],
    "LANDSAT/LC09/C02/T1_L2": ["SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B6", "SR_B7"],
}
NOMBRES_COMUNES = ["azul", "verde", "rojo", "nir", "swir1", "swir2"]

# %% Función: composite (mediana) de una temporada
def composite(ano):
    """Mediana de las fechas despejadas de una temporada, con bandas de nombre común."""
    inicio = ee.Date.fromYMD(ano - 1, 12, 1)
    fin = ee.Date.fromYMD(ano, 3, 1)
    fechas = FECHAS_DESPEJADAS[ano]

    coleccion = ee.ImageCollection([])
    for id_coleccion, bandas in BANDAS.items():
        coleccion_sat = (
            ee.ImageCollection(id_coleccion)
            .filterBounds(area)
            .filterDate(inicio, fin) # para que al hacer la comparación con DATE_ACQUIRED no se demore más
            .filter(ee.Filter.inList("DATE_ACQUIRED", fechas))
            .select(bandas, NOMBRES_COMUNES)
        )
        coleccion = coleccion.merge(coleccion_sat)

    print(ano, "imágenes:", coleccion.size().getInfo())

    return coleccion.median().multiply(0.0000275).add(-0.2).clip(area)

# %% Composites de las 4 temporadas
composites = {}
for ano in TEMPORADAS:
    composites[ano] = composite(ano)

# %% Mapa
vis_falso_color = {"bands": ["swir1", "nir", "rojo"], "min": 0, "max": 0.4}
vis_natural = {"bands": ["rojo", "verde", "azul"], "min": 0, "max": 0.4}

Map = geemap.Map()
Map.centerObject(area, zoom=12)
for ano, imagen in composites.items():
    Map.addLayer(imagen, vis_natural, f"Natural {ano}", False)
    Map.addLayer(imagen, vis_falso_color, f"Falso color {ano}", False)
Map
# %%
