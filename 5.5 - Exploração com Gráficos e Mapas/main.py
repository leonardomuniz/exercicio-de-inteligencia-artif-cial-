# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import zipcodes
import numpy as np
import folium
from folium.plugins import HeatMap


# peaga retorna uma lista conforme o agrupamento
def filter_ocorrencias_by_column_dataframe(dataframe, column, count=4, ascending=True):
    filter = dataframe.groupby([column]).size().reset_index(name='counts')
    filter = filter.sort_values(by='counts', ascending=ascending).head(count)
    filter = filter[column].values
    return filter


# metodo que cria e salva os graficos
def create_grafico_barras(dataframe, set_ylabel="", file="", stacked=False):
    ax = dataframe.plot.bar(rot=0, stacked=stacked)
    ax.set_ylabel(set_ylabel)

    if file:
        fig = ax.get_figure()
        fig.savefig(file)
    return ax


def plotar_grafico(ovnis):
    # pesquisando os quatro estados com maior incidencia de apariçoes
    states = filter_ocorrencias_by_column_dataframe(dataframe=ovnis, column='State', ascending=False)

    # filtrando os estados com maiores aparicoes
    filtred = ovnis[ovnis.State.isin(states)]

    # pesquisando os quatro shapes com maior incidencia de apariçoes nos estados
    shapes = filter_ocorrencias_by_column_dataframe(dataframe=filtred, column='Shape', ascending=False)

    # filtrando shapes com maior numero de aparicoes por estado
    filtred = filtred[filtred.Shape.isin(shapes)]

    # agrupando os shanpes por estado
    grouped = filtred.groupby(['State', 'Shape']).size().reset_index(name='counts')

    # invertendo as colunas para mostrar shapes por estado
    grouped = grouped.pivot_table('counts', ['State'], 'Shape')

    print(grouped)

    grafico1 = create_grafico_barras(grouped, set_ylabel='Views', file='ocorrencias_barras_agrupadas.jpg')
    grafico2 = create_grafico_barras(grouped, set_ylabel='Views', file='ocorrencias_barras_empilhadas.jpg',
                                     stacked=True)

    plt.show()


def buscar_latitude_longitude(dataframe):
    dataframe.City = dataframe.City.str.strip()
    dataframe.State = dataframe.State.str.strip()

    lat_long = {
        "lat": [],
        "long": []
    }

    for i, row in dataframe.iterrows():
        city = row.City
        state = row.State

        cities = zipcodes.filter_by(city=city, state=state)

        if cities:
            lat_long["lat"].append(cities[0]['lat'])
            lat_long["long"].append(cities[0]['long'])
            continue

        lat_long["lat"].append(np.nan)
        lat_long["long"].append(np.nan)

    df = pd.DataFrame(lat_long)
    df.to_csv('lat_long.csv', index=False)

    return df


def visualizar_todas_ocorrencias_no_mapa(dataframe):
    extra_terrestre = dataframe
    extra_terrestre.columns = [col.strip().replace(' ', '').replace(r'/', '') for col in extra_terrestre.columns]

    extra_terrestre.City = extra_terrestre.City.str.strip()
    extra_terrestre.State = extra_terrestre.State.str.strip()

    data_frame = extra_terrestre.groupby(['City', 'State', 'lat', 'long'])

    lat_long = data_frame[['lat', 'long']].fillna(0)

    BBox = [[lat_long.lat.max(), lat_long.long.max()], [lat_long.lat.min(), lat_long.long.min()]]
    np_array = lat_long.to_numpy().tolist()

    mapa = folium.Map(location=[0, 0], zoom_start=13)
    mapa.fit_bounds(BBox)
    HeatMap(np_array, radius=10).add_to(mapa)
    mapa.save("todas_as_ocorrencias.html")


def buscar_e_salvar_latitude_longitude_das_ocorrencias(ovnis):
    ovnis.City = ovnis.City.str.strip()
    ovnis.State = ovnis.State.str.strip()

    lat_long = buscar_latitude_longitude(ovnis)

    ovnis[['lat', 'long']] = lat_long

    print(ovnis)

    ovnis.to_csv('ovnis_with_lat_long.csv', index=False)


def visualizar_ocorrencias_no_mapa_por_estado(dataframe, estado):
    estado_dataframe = dataframe[dataframe['State'] == estado]

    lat_long = estado_dataframe[['lat', 'long']].fillna(0)

    BBox = [[lat_long.lat.max(), lat_long.long.max()], [lat_long.lat.min(), lat_long.long.min()]]
    np_array = lat_long.to_numpy().tolist()

    mapa = folium.Map(location=[0, 0], zoom_start=13)
    mapa.fit_bounds(BBox)
    HeatMap(np_array, radius=10).add_to(mapa)
    mapa.save("ocorrencias_por_estado.html")


def main():
    ovnis = pd.read_csv('OVNIS.csv')
    ovnis.columns = [col.strip().replace(' ', '').replace(r'/', '') for col in ovnis.columns]

    plotar_grafico(ovnis)

    buscar_e_salvar_latitude_longitude_das_ocorrencias(ovnis)

    extra_terrestre = pd.read_csv('ovnis_with_lat_long2.csv')

    visualizar_todas_ocorrencias_no_mapa(extra_terrestre)

    extra_terrestre.City = extra_terrestre.City.str.strip()
    extra_terrestre.State = extra_terrestre.State.str.strip()

    data_frame = extra_terrestre.groupby(['City', 'State', 'lat', 'long']).size().reset_index(name='counts')

    visualizar_ocorrencias_no_mapa_por_estado(data_frame, 'CA')


if __name__ == '__main__':
    main()
