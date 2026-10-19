# %% Conectar con Google Earth Engine y cargar la configuración
import ee
import geemap
import pandas as pd
from a_config import PROYECTO_GEE, AREA_COORDS

ee.Initialize(project=PROYECTO_GEE)
area = ee.Geometry.Rectangle(AREA_COORDS)

# %% Tabla de imágeneras Landsat 7 de la temporada 2009, ordenadas de menos a más nubes
l7_2009 = (
    ee.ImageCollection("LANDSAT/LE07/C02/T1_L2")
    .filterBounds(area)
    .filterDate("2008-12-01", "2009-03-01")
    .sort("CLOUD_COVER")
)

propiedades = ["DATE_ACQUIRED", "WRS_PATH", "WRS_ROW", "CLOUD_COVER"]

datos = (
    l7_2009
    .reduceColumns(ee.Reducer.toList(len(propiedades)), propiedades)
    .get("list")
    .getInfo()
)

tabla_2009 = pd.DataFrame(datos, columns=["fecha", "path", "fila", "nubes_escena_%"])
tabla_2009

# %% Ver una imagen concreta
imagen = (
    l7_2009
    #.filter(ee.Filter.eq("DATE_ACQUIRED", "2009-02-05"))
    .filter(ee.Filter.eq("CLOUD_COVER", 47))
    .first() #Se requiere para elegir la imagen de la colección así sea solo 1
)

reflectancia = imagen.select("SR_B.").multiply(0.0000275).add(-0.2).clip(area)

# Color natural: rojo, verde y azul reales
vis_natural = {"bands": ["SR_B3", "SR_B2", "SR_B1"], "min": 0, "max": 0.4}

# Falso color: SWIR1 en rojo, NIR en verde, rojo visible en azul
vis_falso_color = {"bands": ["SR_B5", "SR_B4", "SR_B3"], "min": 0, "max": 0.4}

Map = geemap.Map()
Map.centerObject(area, zoom=12)
Map.add_basemap("SATELLITE")
Map.addLayer(reflectancia, vis_natural, "Color natural")
Map.addLayer(reflectancia, vis_falso_color, "Falso color (SWIR-NIR-rojo)")
Map

# %%
