# Instalacion primero de gpxpy con 'pip install gpxpy'
import gpxpy
import gpxpy.gpx
# Instalacion a su vez de pandas 'pip install pandas'
import pandas as pd
# pip install matplotlib
import matplotlib.pyplot as plt
# pip install haversine
import haversine as hs
# pip install numpy
import numpy as np

def visualiza(f_gpx):
    with open(f_gpx, 'r', encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    route_info = []

    for track in gpx.tracks:
        print('El nombre de la ruta en cuestion es: ' + track.name)
        print('')
        for segment in track.segments:
                for point in segment.points:
                    route_info.append({
                        'latitude': point.latitude,
                        'longitude': point.longitude,
                        'evelation': point.elevation
                    })

    route_df = pd.DataFrame(route_info)
    print(route_df.head())

    print('Calculamos la diferencia de evelacion entre los puntos')
    input('Haga enter')
    route_df['evelation_dif'] = route_df['evelation'].diff()
    print(route_df.head())
    print('')
    print('A continuación se mostrata una figura que representa la ruta del GPX si fuera sobre un mapa real')
    input('Haga enter')
    plt.figure(figsize=(14,8))
    plt.title('representación en formato mapa', size = 18)
    plt.plot(route_df['longitude'], route_df['latitude'], color='#101010')
    plt.show()
    print('A continuación se mostrata una figura que representa  el desnivel que se ofrece ')
    input('Haga enter')

    distances = [np.nan]
    for i in range(len(route_df)):
        if i == 0:
            continue
        else:
            distances.append(haversine_distance(
                route_df.iloc[i-1]['latitude'],
                route_df.iloc[i-1]['longitude'], 
                route_df.iloc[i]['latitude'],
                route_df.iloc[i]['longitude']
            ))

    route_df['distance'] = distances
    route_df = route_df.fillna(0)
    print(route_df.head())
    print()
    print('A continuacion se muestra una tabla con la informacion de las elevaciones y distancias, para poder representarlo en una grafica')
    route_df['cum_elevation'] = route_df['evelation_dif'].cumsum()
    route_df['cum_distance'] = route_df['distance'].cumsum()
    print(route_df.head())
    print()
    print('A continuacion se muestra una grafica con el perfil de elevacion segun la distancia')
    input('Haga enter')
    plt.plot(route_df['cum_distance'], route_df['cum_elevation'], color='#101010', lw = 3)
    plt.title('perfil de elevación de la ruta', size = 18)
    plt.xlabel('distancia en metros', size = 15)
    plt.ylabel('Elevacion en metros', size = 15)
    plt.show()
    return 0

def haversine_distance(l1, lo1, l2, lo2):
    distance = hs.haversine(
        point1 = (l1, lo1),
        point2 = (l2, lo2), 
        unit = hs.Unit.METERS 
    )
    return np.round(distance, 2)

def checkExist(file):
    try:
        with open(file, 'r') as f:
            return True
    except FileNotFoundError:
        print('No se ha encontrado el archivo, vuelva a intentarlo')
        main();


def main():
    """Metodo que pide por consola el fichero e intenta ejecutar el codigo"""
    print("En este archivo se realiza un analisis del docuemnto, en cuanto adiferencias de alturas,")
    print('además se representa en graficas, como seria la ruta en un mapa, continuando por')
    print('generacion de diferencias de alturas segun van avanzando los kilometros')
    f_gpx = input("Nombre del fichero GPX: ")
    checkExist(f_gpx)
    visualiza(f_gpx)

if __name__ == '__main__':
    main()