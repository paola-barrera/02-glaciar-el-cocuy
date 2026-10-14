# %% Ver el área de estudio sin GEE
import folium

mapa = folium.Map(location=[6.45, -72.285], zoom_start=12)
folium.Rectangle(
    bounds=[[6.33, -72.34], [6.57, -72.23]],  # [[sur, oeste], [norte, este]]
    color="red",
    fill=False,
).add_to(mapa)
mapa