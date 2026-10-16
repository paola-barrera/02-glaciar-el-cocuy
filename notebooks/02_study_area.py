# %% Conectar con Google Earth Engine
import ee
import geemap
from a_config import PROYECTO_GEE, AREA_COORDS, UMBRAL_ALTITUD
ee.Initialize(project=PROYECTO_GEE)

# %% Área de estudio: rectángulo alrededor de la Sierra Nevada del Cocuy
# Fuente: IDEAM, 6°21'-6°33' N y 72°15'-72°19' O, con un margen de 0,02° (~2 km)
# [longitud oeste, latitud sur, longitud este, latitud norte] (paso de grados minutos y segundos a grados decimales en Excel)
area = ee.Geometry.Rectangle(AREA_COORDS)

# %% Elevación: conservar solo el terreno por encima de 4.200 m. Límite superior páramo alto según IGAC comienza con esa altitud
# Modelo de elevación: Copernicus DEM GLO-30
# Se excluyen las teselas del polo sur (S90), que filterBounds devuelve por error
coleccion_dem = (
    ee.ImageCollection("COPERNICUS/DEM/GLO30_2024_1")
    .filterBounds(area)
    .filter(ee.Filter.stringStartsWith("system:index", "S90").Not())
)
proyeccion = coleccion_dem.first().projection()
dem = coleccion_dem.mosaic().setDefaultProjection(proyeccion).select("DEM").clip(area)
limite_paramo = dem.gt(UMBRAL_ALTITUD).selfMask()

# %% Ver el área de estudio y la alta montaña en un mapa
Map = geemap.Map()
Map.add_basemap("SATELLITE")
Map.centerObject(area, zoom=12)
Map.addLayer(limite_paramo, {"palette": ["orange"], "opacity": 0.5}, "Por encima de 4.200 m")
Map.addLayer(area, {"color": "red"}, "Área de estudio")
Map


# %%
