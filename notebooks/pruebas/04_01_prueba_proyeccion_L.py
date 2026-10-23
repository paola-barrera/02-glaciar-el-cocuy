# %% Conectar con Google Earth Engine y cargar la configuración
import ee
from a_config import PROYECTO_GEE, AREA_COORDS
ee.Initialize(project=PROYECTO_GEE)
area = ee.Geometry.Rectangle(AREA_COORDS)



# %% ¿En qué proyección viene Landsat en el Cocuy?
imagen = (
    ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
    .filterBounds(area)
    .filter(ee.Filter.eq("DATE_ACQUIRED", "2024-01-06"))
    .first()
)
print(imagen.select("SR_B4").projection().getInfo())