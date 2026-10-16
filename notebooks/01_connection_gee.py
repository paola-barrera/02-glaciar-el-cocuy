# %% Importar la librería de Google Earth Engine
import ee
from a_config import PROYECTO_GEE

# %% Iniciar sesión 
ee.Authenticate()

# %% Conectar con proyecto de Google Cloud
ee.Initialize(project=PROYECTO_GEE)

# %% Comprobar la conexión
print(ee.String("Conectado a Google Earth Engine").getInfo())
# %%
