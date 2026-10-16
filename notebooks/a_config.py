"""Parámetros proyecto"""

# Proyecto de Google Earth Engine
PROYECTO_GEE = "tactical-runway-463615-m4"

# Área de estudio: [longitud oeste, latitud sur, longitud este, latitud norte] (paso de grados minutos y segundos a grados decimales en Excel)
# Fuente: IDEAM, 6°21'-6°33' N y 72°15'-72°19' O, con un margen de 0,02° (~2 km)
AREA_COORDS = [-72.34, 6.33, -72.23, 6.57]

# Umbral de altitud (m): límite superior del páramo alto (IGAC)
UMBRAL_ALTITUD = 4200