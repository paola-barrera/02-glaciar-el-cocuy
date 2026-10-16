# %% Conectar con Google Earth Engine
import ee
import pandas as pd
from a_config import PROYECTO_GEE, AREA_COORDS
ee.Initialize(project=PROYECTO_GEE)

# %% Área de estudio 
area = ee.Geometry.Rectangle(AREA_COORDS)

# %% Colecciones Landsat
colecciones = {
    "L5": "LANDSAT/LT05/C02/T1_L2",
    "L7": "LANDSAT/LE07/C02/T1_L2",
    "L8": "LANDSAT/LC08/C02/T1_L2",
    "L9": "LANDSAT/LC09/C02/T1_L2",
}

# %% Contar imágenes de cada año por temporada seca y % de nubes
# La temporada seca va de diciembre del año anterior a febrero del año analizado
def resumen_ano(ano):
    inicio = ee.Date.fromYMD(ano - 1, 12, 1)
    fin = ee.Date.fromYMD(ano, 3, 1)
    conteos = {}
    conteos["año"] = ano
    for nombre, id_coleccion in colecciones.items():
        coleccion = ee.ImageCollection(id_coleccion).filterBounds(area).filterDate(inicio, fin)
        conteos[f"{nombre} total"] = coleccion.size()
        conteos[f"{nombre} <50% nubes"] = coleccion.filter(ee.Filter.lt("CLOUD_COVER", 50)).size()
    resultado = ee.Dictionary(conteos).getInfo()
    return resultado

#%%
filas = [resumen_ano(ano) for ano in range(2009, 2027)]
tabla = pd.DataFrame(filas).set_index("año")
tabla

# %%
