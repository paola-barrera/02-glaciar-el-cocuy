# %% Conectar con Google Earth Engine y cargar la configuración
import sys
sys.path.append("..") #Para buscar en carpeta de arriba y no en /pruebas

import ee
import geemap
from a_config import PROYECTO_GEE, AREA_COORDS

ee.Initialize(project=PROYECTO_GEE)
area = ee.Geometry.Rectangle(AREA_COORDS)

# %% Imágenes Landsat 7 de la temporada 2009
l7_2009 = (
    ee.ImageCollection("LANDSAT/LE07/C02/T1_L2")
    .filterBounds(area)
    .filterDate("2008-12-01", "2009-03-01")
)
# %% Mediana de las 3 fechas despejadas (elegidas a mano)
fechas_buenas = ["2008-12-19", "2009-01-04", "2009-02-21"]

seleccion = l7_2009.filter(ee.Filter.inList("DATE_ACQUIRED", fechas_buenas))
print("Imágenes seleccionadas:", seleccion.size().getInfo())
mediana = seleccion.median()
reflectancia_mediana = mediana.select("SR_B.").multiply(0.0000275).add(-0.2).clip(area)

# Una sola imagen (4 de enero, fila 56), para comparar
una_imagen = (
    l7_2009
    .filter(ee.Filter.eq("DATE_ACQUIRED", "2009-01-04"))
    .filter(ee.Filter.eq("WRS_ROW", 56))
    .first()
)
reflectancia_una = una_imagen.select("SR_B.").multiply(0.0000275).add(-0.2).clip(area)

# %% Mapa para comparar
# Color natural: rojo, verde y azul reales
vis_natural = {"bands": ["SR_B3", "SR_B2", "SR_B1"], "min": 0, "max": 0.4}
# Falso color: SWIR1 en rojo, NIR en verde, rojo visible en azul
vis_falso_color = {"bands": ["SR_B5", "SR_B4", "SR_B3"], "min": 0, "max": 0.4}

Map = geemap.Map()
Map.centerObject(area, zoom=12)
Map.add_basemap("SATELLITE")
Map.addLayer(reflectancia_una, vis_falso_color, "Solo 2009-01-04")
Map.addLayer(reflectancia_mediana, vis_falso_color, "Mediana de 3 fechas")
Map.addLayer(reflectancia_mediana, vis_natural, "Color natural")
Map
# %%
