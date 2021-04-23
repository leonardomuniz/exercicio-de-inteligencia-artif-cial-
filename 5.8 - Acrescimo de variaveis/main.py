# -*- coding: utf-8 -*-
import pandas as pd
import datetime


def traduzir_dia_da_semana(dia):
    dias = {
        'Monday': 'Segunda-Feira',
        'Tuesday': 'Terça-Feira',
        'Wednesday': 'Quarta-Feira',
        'Thursday': 'Quinta-Feira',
        'Friday': 'Sexta-Feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    if dia not in dias.keys():
        return dia

    return dias[dia.strip()]


def main():
    ovnis = pd.read_csv('df_OVNI_limpo.csv')
    ovnis.columns = [col.strip().replace(' ', '').replace(r'/', '') for col in ovnis.columns]

    # separando date e time em duas colunas
    ovnis[['Sight_Date', 'Sigth_Time']] = ovnis['DateTime'].str.split(' ', 1, expand=True)

    # remover colunas desnecessarias
    ovnis.drop(['DateTime', 'row', 'Unnamed:0'], axis='columns', inplace=True)

    # converte a cluna para o tipo data
    ovnis['Sight_Date'] = pd.to_datetime(ovnis['Sight_Date'])

    # separa a coluna dos dias
    ovnis[['Sight_Day']] = ovnis['Sight_Date'].dt.strftime("%d")

    # separa a coluna dos meses
    ovnis[['Sight_Month']] = ovnis['Sight_Date'].dt.strftime("%m")

    # criar coluna com nome dos dias da semanda
    ovnis[['Sight_WeekDate']] = ovnis['Sight_Date'].dt.strftime("%A")

    # traduzir os dias da semana para pt-br
    ovnis['Sight_WeekDate'] = ovnis['Sight_WeekDate'].apply(lambda dia: traduzir_dia_da_semana(dia))

    # converter data para o padaro brasileiro
    ovnis['Sight_Date'] = ovnis['Sight_Date'].dt.strftime('%d/%m/%Y')

    ovnis.to_csv('df_OVNI_preparado.csv', mode='a', header=True)

    print(ovnis)


if __name__ == '__main__':
    main()
