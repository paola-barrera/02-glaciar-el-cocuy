# %% Conectar con Google Earth Engine y cargar la configuración
import ee
import geemap
import pandas as pd
from a_config import PROYECTO_GEE, AREA_COORDS

ee.Initialize(project=PROYECTO_GEE)
area = ee.Geometry.Rectangle(AREA_COORDS)


# %%
