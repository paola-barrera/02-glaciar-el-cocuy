"""Parámetros proyecto"""

# Proyecto de Google Earth Engine
PROYECTO_GEE = "tactical-runway-463615-m4"

# Temporadas del proyecto: 2009 y 2026 (relato), 2010 y 2024 (validación con el IDEAM)
TEMPORADAS = [2009, 2010, 2024, 2026]

# Área de estudio: [longitud oeste, latitud sur, longitud este, latitud norte] (paso de grados minutos y segundos a grados decimales en Excel)
# Fuente: IDEAM, 6°21'-6°33' N y 72°15'-72°19' O, con un margen de 0,02° (~2 km)
AREA_COORDS = [-72.34, 6.33, -72.23, 6.57]

# Umbral de altitud (m): límite superior del páramo alto (IGAC)
UMBRAL_ALTITUD = 4200

# Fechas con el glaciar despejado, elegidas a mano por temporada (año = enero)
FECHAS_DESPEJADAS = {
    2009: ["2008-12-19", "2009-01-04", "2009-02-21"], # L7
    2010: ["2009-12-06", "2009-12-14"],  # L7 y L5
    2011: ["2011-01-26"],  # L7 solo una fecha: las franjas no se rellenan. 2011-01-10 parece tener nube en el centro del glaciar
    2012: ["2012-02-14"],  # L7 solo una fecha: las franjas no se rellenan. 2012-01-29 tiene nubes en los picos pequeños
    2013: ["2012-12-14", "2012-12-30", "2013-01-15"],  # L7 2013-01-31 descartada: nubes en picos pequeños
    2014: ["2014-01-10", "2014-02-11"],  # L8. L7 2014-02-03 también despejada: útil para comparar sensores
    2024: ["2023-12-05", "2023-12-13", "2024-01-06", "2024-01-14", "2024-01-22"],  # L8 y L9. L7 no valía la pena
    2026: ["2025-12-18", "2025-12-26", "2026-02-12", "2026-02-28"],  # L8 y L9
}

# Umbrales para clasificar hielo (algoritmos clásicos de nieve; comprobados en 2009 y 2026)
UMBRAL_NDSI = 0.4   # por encima: nieve, hielo o agua
UMBRAL_NIR = 0.11   # por encima: descarta el agua, que es muy baja en el NIR