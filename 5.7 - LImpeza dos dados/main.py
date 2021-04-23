import pandas as pd
import numpy as np

#coleta de dados dos ovnis
dados_ovni = pd.read_csv('OVNIS.csv')


#transformar os dados em um data frame e limpeza dos dados
tabela_ovni = pd.DataFrame(dados_ovni)
tabela_ovni.fillna(method='ffill').dropna()


#filtragem das colunas principais para a tabela
filtro_tabela = ['row','Date / Time','State','Shape','City']
tabela_filtrada = tabela_ovni.filter( items = filtro_tabela)


#coleta das formas de shape mais populares que possuem mais de 1000 reigstros
shape_filtrado = tabela_filtrada.groupby('Shape').count()
shape_filtrado = shape_filtrado['row'].sort_values(ascending=False)
shape_filtrado = shape_filtrado[shape_filtrado >1000]
shape_filtrado = shape_filtrado.to_frame()
lista_shapes = shape_filtrado.index.tolist()


# coleta dos estados
estados_permitidos = pd.read_excel('states.xlsx')


#transformação da tabela de estados
transformacao_tabela_estados = estados_permitidos["State"].str.split(',')


#transformação dos dados coletados e inserção das novas colunas no data frame
estado = transformacao_tabela_estados.str.get(0)
abreviacao = transformacao_tabela_estados.str.get(1)
estados_permitidos["Estado"] = estado
estados_permitidos["Abreviação"] = abreviacao.str.replace('"','')
estados = estados_permitidos[['Estado','Abreviação']]
lista_estados = estados['Abreviação'].tolist()


#transformação das tabelas tratadas em csv
data_frame = tabela_filtrada[(tabela_filtrada.State.isin(lista_estados)) & (tabela_filtrada.Shape.isin(lista_shapes))]
data_frame.to_csv('df_OVNI_limpo.csv', mode='w', header=True)

