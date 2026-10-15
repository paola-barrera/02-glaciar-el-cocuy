# %% Conectar con Google Earth Engine
import ee
import pandas as pd
ee.Initialize(project="tactical-runway-463615-m4")

# %% Área de estudio 
area = ee.Geometry.Rectangle([-72.34, 6.33, -72.23, 6.57])

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
filas = [resumen_anio(anio) for anio in range(2009, 2027)]
tabla = pd.DataFrame(filas).set_index("año")
tabla
