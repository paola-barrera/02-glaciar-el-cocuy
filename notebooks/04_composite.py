# %% Conectar con Google Earth Engine y cargar la configuración
import ee
import geemap
from a_config import PROYECTO_GEE, AREA_COORDS, FECHAS_DESPEJADAS, TEMPORADAS, UMBRAL_NDSI, UMBRAL_NIR, UMBRAL_ALTITUD

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

    return coleccion.median().multiply(0.0000275).add(-0.2).clamp(0, 1).clip(area)

# %% Modelo de elevación 
coleccion_dem = (
    ee.ImageCollection("COPERNICUS/DEM/GLO30_2024_1")
    .filterBounds(area)
    .filter(ee.Filter.stringStartsWith("system:index", "S90").Not())
)
proyeccion = coleccion_dem.first().projection()
dem = coleccion_dem.mosaic().setDefaultProjection(proyeccion).select("DEM").clip(area)

# %% Composites, NDSI y nieve de las 4 temporadas
composites = {}
for ano in TEMPORADAS:
    composites[ano] = composite(ano)

ndsi = {}
for ano, imagen in composites.items():
    ndsi[ano] = imagen.normalizedDifference(["verde", "swir1"]).rename("ndsi")

# Polígono dibujado manualmente tras revisión visual. Incluye zona clasificada como nieve que no es nieve. Problema de toma de datos de Landsat 7
zona_excluida = geemap.geojson_to_ee("../data/zona_excluida.geojson")
fuera_de_zona = ee.Image(1).paint(zona_excluida, 0)

nieve = {}
for ano in TEMPORADAS:
    nieve[ano] = (
        ndsi[ano].gt(UMBRAL_NDSI)
        .And(composites[ano].select("nir").gt(UMBRAL_NIR))
        .And(dem.gt(UMBRAL_ALTITUD))
        .And(fuera_de_zona)
        .rename("nieve")
    )

# %% Mapa
vis_falso_color = {"bands": ["swir1", "nir", "rojo"], "min": 0, "max": 0.6}
vis_natural = {"bands": ["rojo", "verde", "azul"], "min": 0, "max":0.6}
vis_ndsi = {"min": -1, "max": 1, "palette": ["olive", "lightgray", "blue"]} #no es necesario poner una sola banda porque no hay canales para ponerle los colores


TEMPORADAS = [2026]

Map = geemap.Map()
Map.centerObject(area, zoom=12)
Map.add_basemap("SATELLITE")
for ano in TEMPORADAS:
    Map.addLayer(dem.gt(UMBRAL_ALTITUD).selfMask(), {"palette": ["red"], "opacity": 0.5}, "Por encima de 4.200 m", False)
    Map.addLayer(composites[ano], vis_natural, f"Natural {ano}", False)
    Map.addLayer(composites[ano], vis_falso_color, f"Falso {ano}", False)
    Map.addLayer(ndsi[ano], vis_ndsi, f"NDSI {ano}", False)
    Map.addLayer(nieve[ano].selfMask(), {"palette": ["orange"]}, f"Nieve {ano}", False)
Map

TEMPORADAS = [2009, 2010, 2024, 2026]
#%%Hacer un split de mapas
''' 
izquierda = geemap.ee_tile_layer(ndsi[2009], vis_ndsi, "NDSI 2009")
derecha = geemap.ee_tile_layer(ndsi[2026], vis_ndsi, "NDSI 2026")

Map = geemap.Map()
Map.centerObject(area, zoom=12)
Map.split_map(left_layer=izquierda, right_layer=derecha)
Map

'''
# %% Descargar la máscara de nieve de 2009 y su composite
geemap.ee_export_image(
    nieve[2009].toByte(),
    filename="../data/nieve_2009.tif",
    region=area,
    scale=30,
    crs="EPSG:4326",
)

geemap.ee_export_image(
    composites[2009].select(["swir1", "nir", "rojo"]).toFloat(),
    filename="../data/falso_color_2009.tif",
    region=area,
    scale=30,
    crs="EPSG:4326",
)

# %%
