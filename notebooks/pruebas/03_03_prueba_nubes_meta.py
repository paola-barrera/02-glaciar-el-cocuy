# %% Conectar con Google Earth Engine y cargar la configuración
import sys
sys.path.append("..")

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

# %% Una fecha con nubes sobre el glaciar: 3 de diciembre de 2008, fila 56
imagen = (
    l7_2009
    .filter(ee.Filter.eq("DATE_ACQUIRED", "2009-02-21"))
    .filter(ee.Filter.eq("WRS_ROW", 56))
    .first()
)

reflectancia = imagen.select("SR_B.").multiply(0.0000275).add(-0.2).clip(area)

# %% Máscara de nubes según QA_PIXEL (bit 3) según manuales USGC
qa = imagen.select("QA_PIXEL")
nube = qa.bitwiseAnd(1 << 3).neq(0)

# %% Mapa
vis_falso_color = {"bands": ["SR_B5", "SR_B4", "SR_B3"], "min": 0, "max": 0.4}

Map = geemap.Map()
Map.centerObject(area, zoom=12)
Map.add_basemap("SATELLITE")
Map.addLayer(reflectancia, vis_falso_color, "2008-12-03, fila 56")
Map.addLayer(nube.selfMask().clip(area), {"palette": ["red"]}, "Nube según QA_PIXEL", False)
Map


# No continuamos con este método porque se identifica como nube los bordes del glaciar, 
# lo cual podría disminuir el área. Lo más efectivo sería evaluar adicionalmente otros intervalos de confianza
# Para este proyecto, no lo vamos a hacer