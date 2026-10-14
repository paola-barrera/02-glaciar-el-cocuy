# %% Importar la librería de Google Earth Engine
import ee

# %% Iniciar sesión 
ee.Authenticate()

# %% Conectar con proyecto de Google Cloud
ee.Initialize(project="tactical-runway-463615-m4")

# %% Comprobar la conexión
print(ee.String("Conectado a Google Earth Engine").getInfo())
# %%
