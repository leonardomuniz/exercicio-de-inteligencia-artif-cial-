# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt


def plotar_grafic_bar_views_by_mes(ovnis, year):
    df = pd.DataFrame(ovnis['Sight_Date']).reset_index()

    df = df[df['Sight_Date'].dt.year == year]

    df = df.groupby(df['Sight_Date'].dt.month_name(), sort=False)['Sight_Date'].count().reset_index(name='views')

    ax = df.plot.bar(rot=0, stacked=False, x='Sight_Date', y='views')
    ax.set_ylabel("Views")

    fig = ax.get_figure()
    fig.savefig("grafico_aparicoes_meses.jpg")

    print(df)


def plotar_grafic_line_views_by_year(ovnis):
    df = ovnis.groupby(ovnis['Sight_Date'].dt.year, sort=False)['Sight_Date'].count().reset_index(name='views')

    df['Sight_Date'] = df['Sight_Date'].astype(str)

    ax = df.plot.line(rot=0, stacked=False, x='Sight_Date', y='views')
    ax.set_ylabel("Views")

    fig = ax.get_figure()
    fig.savefig("grafico_aparicoes_anos.jpg")

    print(df)


def resolucao_parte_um():
    ovnis = pd.read_csv('df_OVNI_preparado.csv')

    ovnis['City'].fillna("", inplace=True)

    ovnis = ovnis[ovnis['City'].str.lower() == "phoenix"]

    ovnis[['Sight_Date']] = pd.to_datetime(ovnis['Sight_Date'], format='%d/%m/%Y')

    ovnis.sort_values(by='Sight_Date', inplace=True)

    plotar_grafic_bar_views_by_mes(ovnis, 2017)

    plotar_grafic_line_views_by_year(ovnis)

    plt.show()


def main():
    resolucao_parte_um()


if __name__ == '__main__':
    main()
