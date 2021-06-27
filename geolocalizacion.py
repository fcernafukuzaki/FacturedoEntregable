# ENTREGABLE Test2 Data Engineer
#
# Autor: Francisco Cerna Fukuzaki
#
# ==============================================================================

# Uso de librería para obtener latitud y longitud a partir de la dirección
# Fuente: https://pypi.org/project/geopy/
# !pip install geopy

# Uso de la librería folium para mostrar las ubicaciones en un mapa
# Fuente: https://python-visualization.github.io/folium/quickstart.html#Getting-Started
# !pip install folium

import pandas as pd
from geopy.geocoders import Nominatim
import folium

UBICACION_ARCHIVO = './addresses_sweden.csv'

contenido = pd.read_csv(UBICACION_ARCHIVO)
contenido.head()

locator = Nominatim(user_agent="test-francisco")

contenido['latitud'] = contenido['ADDRESS'].apply(lambda address: locator.geocode(address).latitude if locator.geocode(address) is not None else None)
contenido['longitud'] = contenido['ADDRESS'].apply(lambda address: locator.geocode(address).longitude if locator.geocode(address) is not None else None)

contenido.head(8)

'''
Análisis exploratorio de la data

No se logró obtener la latitud y longitud de los registros con índice 7 y 21.
Por lo que se realiza pruebas con la dirección ingresada para validar que exista y sea reconocida por la libería.
De esta forma se llega a la conclusión que se debe reemplazar algunas partes de la dirección.
'''
print(contenido['ADDRESS'][contenido['latitud'].isnull()])

print(contenido['ADDRESS'][7].replace("7-9","7"))
address = locator.geocode(contenido['ADDRESS'][7].replace("7-9","7"))
print(address)

datos_ubicacion = locator.geocode(address)
contenido['latitud'][7] = datos_ubicacion.latitude if datos_ubicacion is not None else None
contenido['longitud'][7] = datos_ubicacion.longitude if datos_ubicacion is not None else None

print(contenido['ADDRESS'][21])
address = locator.geocode(contenido['ADDRESS'][21].replace("plan ", ""))
print(address)

datos_ubicacion = locator.geocode(address)
contenido['latitud'][21] = datos_ubicacion.latitude if datos_ubicacion is not None else None
contenido['longitud'][21] = datos_ubicacion.longitude if datos_ubicacion is not None else None

contenido.head(8)

# Obtener mapa del mundo y ubicar el mapa con la latitud y longitud del primer registro
mapa = folium.Map(
    location=[contenido['latitud'][0], contenido['longitud'][0]],
    zoom_start=13,
)
# Mostrar las ubicaciones en el mapa
contenido.apply(lambda row : folium.Marker(location=[row['latitud'], row['longitud']]).add_to(mapa), axis=1)
mapa
