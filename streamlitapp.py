'''
FUNCIONALIDADES DA APLICAÇÃO

- VISUALIAÇÕES
    . correlações (seletor de váriaveis X e Y) --- DONE
    . countplot -- DONE
    . ECDF --- DONE
    . estatísticas (min, max, med, mean)

- FILTROS
    . filtro por data (match id) --- DONE
    . agentes, times, mapas --- DONE

- INTERAÇÕES
    . download de tabelas -- DONE
    . download de gráficos -- DIFICIL
    . acesso externo (via deploy github)

'''
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessamento import Preproc


def FilterJogadores(df, id, times, agentes, mapas):

    if len(times) > 0: df = df[df['Time'].isin(times)]
    if len(agentes) > 0: df = df[df['Agente'].isin(agentes)]
    if len(mapas) > 0: df = df[df['Mapa'].isin(mapas)]
    df_antes = df[df['ID Partida'] <= id]
    df_depois = df[df['ID Partida'] >= id]

    return df_antes, df_depois

def FilterTimes(df, id, times, mapas):

    if len(times) > 0: df = df[df['Time'].isin(times)]
    if len(mapas) > 0: df = df[df['Mapa'].isin(mapas)]
    df_antes = df[df['ID Partida'] <= id]
    df_depois = df[df['ID Partida'] >= id]

    return df_antes, df_depois

def ECDFPlot(df, col):

    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 9,
          'axes.labelsize': 12,
          'xtick.labelsize': 9,
          'ytick.labelsize': 14}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()

    ax = sns.ecdfplot(data=df, x=col, color='#f94555')
    #plt.axvline(df[col].mean(), 0,1, color='white')
    plt.xlabel('Valor')
    plt.ylabel('Proporção')
    plt.title(f'Distribuição Cumulativa de {col}')
    st.pyplot(fig)

def Distplot(df, col):

    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 9,
          'axes.labelsize': 12,
          'xtick.labelsize': 9,
          'ytick.labelsize': 14}
    
    plt.rcParams.update(rc)
    bins =  1 + 3.322*np.log(df[col].nunique())
    fig, ax = plt.subplots()
    
    ax = sns.histplot(data=df, x=col, bins=int(bins), color='#dc3d4b')
    #plt.axvline(df[col].mean(), 0,1, color='white')
    
    ax.set_title(f'Distribuição de {col}', fontsize = 16)
    ax.set_xlabel(col, fontsize = 12)
    ax.tick_params(rotation = 20, axis = 'x')
    ax.set_ylabel('Quantidade', fontsize = 12)
    
    st.pyplot(fig)
    #DownloadPlot(ax)

def Countplot(df, col,num_obj):

    ## filtrando por top N mais frequentes
    dados_plot = df[df[col].isin( list(df[col].value_counts()[:num_obj].index) )]
    
    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 9,
          'axes.labelsize': 12,
          'xtick.labelsize': 9,
          'ytick.labelsize': 14}
    
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ax = sns.countplot(y = col, 
                        data = dados_plot, order=dados_plot[col].value_counts().index, 
                        palette=['#f94555', '#f2636b', '#672e37', '#7e7c7d', '#ce9e9c'])
    ax.set_title(str(col), fontsize = 16)
    ax.set_xlabel('Quantidade', fontsize = 12)
    ax.tick_params(rotation = 20, axis = 'x')
    ax.set_ylabel(col, fontsize = 12)
  
    st.pyplot(fig)

def CorrPlot(df, cols, data='player'):
    
    if data == 'player': cols = cols
    else: cols = cols = cols + ['Win Rate']
    corr_spearman = round(df[cols].corr(method='pearson'),3)
    mask = np.zeros_like(corr_spearman)
    mask[np.triu_indices_from(mask)] = True
    fig,ax = plt.subplots()
    
    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 9,
          'axes.labelsize': 12,
          'xtick.labelsize': 9,
          'ytick.labelsize': 14}
    
    plt.rcParams.update(rc)

    ax = sns.heatmap(corr_spearman,  fmt="f", vmin=0, vmax=1, mask=mask, annot=True)
    st.pyplot(fig)

def DownloadPlot(fig):

    buffer = StringIO()
    fig.write_html(buffer, include_plotlyjs='cdn')
    html_bytes = buffer.getvalue().encode()

    st.download_button(
            label='Download Plot via HTML',
            data=html_bytes,
            file_name='plot.html',
            mime='text/html'
        )

@st.cache
def DfToCSV(df):
    return df.to_csv(index=False).encode('utf-8')

def DownloadCSV(csv_file, btn_label, file_name):
    st.download_button(
        label=btn_label,
        data=csv_file,
        file_name=file_name,
        mime='text/csv'
)

## Funcao preprocessamento (leitura de arquivo e format de datasets)
df_jogadores, df_times = Preproc()

TIMES = df_times.Time.unique()
AGENTES = df_jogadores.Agente.unique()
MAPAS = df_times.Mapa.unique()
ID_PARTIDA = df_times['ID Partida'].unique()
TITLE = "INTERFACE WEB DE VISUALIZAÇÃO DE ESTATÍSTICAS DO CENÁRIO COMPETITIVO BRASILEIRO DE VALORANT"

st.set_page_config(page_title=TITLE,layout='wide')
f'''# {TITLE} '''

'''---'''

##QUAIS FILTROS EU QUERO PARA OS DADOS
# TIMES
# AGENTES
# MAPAS
# "DATA" - POR MATCH_ID. EXPLICAR AS DATAS
 
st.sidebar.markdown(
'''
## Filtros de Dados

Os filtros a seguir podem ser utilizados para selecionar Partidas, Mapas, Times, ou Agentes específicos para se gerar um conjunto
de dados específico para uma análise mais direcionada. 

Como não foi possível extrair a data exata de cada partida o "Match ID" é utilizado
como filtro temporal, partidas no ano de 2020 possuem um ID menor que 7000.
'''
)

filtro_times = st.sidebar.multiselect('Filtro de Times', TIMES)
filtro_agentes = st.sidebar.multiselect('Filtro de Agentes', AGENTES)
filtro_mapas = st.sidebar.multiselect('Filtro de Mapas', MAPAS)
filtro_id = st.sidebar.select_slider('Filtro de Partidas por ID',  options=df_times['ID Partida'].unique())

## Sidebar -----------------------
st.sidebar.markdown(''' --- 
## Filtros dos gráficos de Times ''')
col_count_time = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Contagem - Times', options = df_times.select_dtypes(include=['object']).columns, index=1)
col_dist_time = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Distribuição - Times', options = df_times.select_dtypes(exclude=['object']).columns, index=1)
cols_corr_time = st.sidebar.multiselect('Seleciona as colunas para o gráfico de Correlação - Times', options = df_times.columns, default=['Win Rate', 'Win Rate ATK', 'Win Rate DEF'])
num_obj = st.sidebar.slider('Quantidade de valores do gráfico de Contagem - Times', min_value=1, max_value=20, value=20)

st.sidebar.markdown(''' --- 
## Filtros dos gráficos de Jogadores ''')

col_count_jogador = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Contagem - Jogadores', options = df_jogadores.select_dtypes(include=['object']).columns)
col_dist_jogador = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Distribuição - Jogadores', options = df_jogadores.select_dtypes(exclude=['object']).columns)
cols_corr_jogador = st.sidebar.multiselect('Seleciona as colunas para o gráfico de Correlação - Jogadores', options = df_jogadores.columns, default=['ACS', 'First Kill Por Round', 'First Death Por Round'])

## -------------------------------

## Amostra das bases
'''## Amostras de Dados'''
'''Uma breve amostra dos dados utilizados no desenvolvimento das análises e visuallizações disponíveis na interface. 
Dados dos times são compostos por somas e médias dos dados dos jogadores deste para uma determinada partida.'''

''' ### Dados de Times '''
st.write(df_times.sample(20, replace=True))
DownloadCSV(DfToCSV(df_times), 
            'Baixar Conjunto de Dados de Jogadores',
            'jogadores.csv')

''' ### Dados de Jogadores'''
st.write(df_jogadores.sample(20,replace=True))
DownloadCSV(DfToCSV(df_jogadores), 
            'Baixar Conjunto de Dados de Times',
            'times.csv')

st.markdown('''---''')

## Dados Times Filtrados
'''## Dados Filtrados Times'''
row2_1, row2_2 = st.columns(2)
filter_times_antigo, filter_times_novo = FilterTimes(df_times, filtro_id, filtro_times, filtro_mapas)
with row2_1:
    f'''### Times - Antes ID {filtro_id}'''
    st.write(f'Total de Linhas - {filter_times_antigo.shape[0]}')
    st.write(filter_times_antigo)
    DownloadCSV(DfToCSV(filter_times_antigo), 
                'Baixar Dados Filtrados',
                'times_filtrados_antesID.csv')
with row2_2:
    f'''### Times - Depois ID {filtro_id}'''
    st.write(f'Total de Linhas - {filter_times_novo.shape[0]}')
    st.write(filter_times_novo)
    DownloadCSV(DfToCSV(filter_times_novo), 
                'Baixar Dados Filtrados',
                'times_filtrados_depoisID.csv')


## Graficos de Contagem Times -- Antes x Depois
'''
## Gráficos de Contagem - Times
São utilizados para se comparar quantidades absolutas entre diferentes valores de um atributo. Por exemplo querendo-se comprara a quantidade de mapas disputados por um determinado time ou 
quantas vezes um determinado agente foi selecionado nas partidas em 2020. Aqui tem-se dados separados por partidas antes e depois de um determiado ID selecionado.
'''

row3_1, row3_2  = st.columns(2)
with row3_1:
    f'''### Dados Antes ID {filtro_id}'''
    Countplot(filter_times_antigo, col_count_time, num_obj)
with row3_2:
    f'''### Dados Após ID {filtro_id}'''
    Countplot(filter_times_novo, col_count_time, num_obj)

## Graficos de Distribuicao Times -- Antes x Depois
'''
## Gráficos de Distribuição - Times
Utilizados para se observar como um conjunto de valores está disitrbuido ao longo de um intervalo, sendo possível identificar intervalos de maior concetração
de observaçoes e em quais intervalos existem observaçoes menos frequentes.

Dentre as opções disponíveis - ECDF e Histograma - tem-se o gráfico de distribuição cumulativa 
([ECDF](https://towardsdatascience.com/what-why-and-how-to-read-empirical-cdf-123e2b922480 "ECDF - Towards Data Sciente")) 
para se observar para qual valor X temos até Y das observaços da amostra
e o Histograma, apresentando faixas de agrupamentos de valores onde quanto maior a faixa mais valores temos dentro desta.
'''
dist_type_time = st.radio("ECDF ou Histograma", options=['ECDF', 'Histograma'])
row4_1, row4_2  = st.columns(2)
with row4_1:
    f'''### Dados Antes ID {filtro_id}'''
    f'''Valor Mínimo - {filter_times_antigo[col_dist_time].min()}'''
    f'''Média - {round(filter_times_antigo[col_dist_time].mean(), 2)}'''
    f'''Mediana - {round(filter_times_antigo[col_dist_time].median(), 2)}'''
    f'''Valor Máximo - {filter_times_antigo[col_dist_time].max()}'''

    if dist_type_time == 'ECDF': ECDFPlot(filter_times_antigo, col_dist_time)
    else: Distplot(filter_times_antigo, col_dist_time)

with row4_2:
    f'''### Dados Após ID {filtro_id}'''
    f'''Valor Mínimo - {filter_times_novo[col_dist_time].min()}'''
    f'''Média - {round(filter_times_novo[col_dist_time].mean(), 2)}'''
    f'''Mediana - {round(filter_times_novo[col_dist_time].median(), 2)}'''
    f'''Valor Máximo - {filter_times_novo[col_dist_time].max()}'''

    if dist_type_time == 'ECDF': ECDFPlot(filter_times_novo, col_dist_time)
    else: Distplot(filter_times_novo, col_dist_time)

'''
## Gráficos de Correlação

Utilizados para apresentar o cálulo da correlação linear de [Spearman](https://towardsdatascience.com/clearly-explained-pearson-v-s-spearman-correlation-coefficient-ada2f473b8 "Correlação de Spearman - Towards Data Science"),
que representa quão relacionado são os valores entre duas variáveis numéricas contínuas. Quanto mais próximo de -1 ou 1 os cálculos, maior é esse relação, negativa ou positiva respectivamente.
'''
row5_1, row5_2  = st.columns(2)
with row5_1:
    f'''### Dados Antes ID {filtro_id}'''
    CorrPlot(filter_times_antigo, cols_corr_time, data='time')
with row5_2:
    f'''### Dados Após ID {filtro_id}'''
    CorrPlot(filter_times_novo, cols_corr_time, data='time')

st.markdown('''---''')
filter_jogador_antigo, filter_jogador_novo = FilterJogadores(df_jogadores, filtro_id, filtro_times, filtro_agentes, filtro_mapas)

## Dados Jogadores Filtrados
'''## Dados Filtrados Jogadores'''
row5_1,  row5_2  = st.columns(2)
with row5_1:
    f'''### Antes ID {filtro_id}'''
    st.write(f'Total de Linhas - {filter_jogador_antigo.shape[0]}')
    st.write(filter_jogador_antigo)
    DownloadCSV(DfToCSV(filter_jogador_antigo), 
                'Baixar Dados Filtrados',
                'jogadores_filtrados_antesID.csv')
with row5_2:
    f'''### Depois ID {filtro_id}'''
    st.write(f'Total de Linhas - {filter_jogador_novo.shape[0]}')
    st.write(filter_jogador_novo)
    DownloadCSV(DfToCSV(filter_jogador_novo), 
                'Baixar Dados Filtrados',
                'jogadores_filtrados_depoisID.csv')


'''## Gráficos de Contagem - Jogadores'''
row6_1,  row6_2  = st.columns(2)
## Graficos de Contagem Times -- Antes x Depois
with row6_1:
    f'''### Dados Antes ID {filtro_id}'''
    Countplot(filter_jogador_antigo, col_count_jogador, num_obj)
with row6_2:
    f'''### Dados Após ID {filtro_id}'''
    Countplot(filter_jogador_novo, col_count_jogador, num_obj)


## Graficos de Contagem Jogadores -- Antes x Depois
'''## Gráficos de Distribuição - Jogadores'''
dist_type_jogador = st.radio("", options=['ECDF', 'Histograma'])
row7_1,  row7_2  = st.columns(2)
with row7_1:
    f'''### Dados Antes ID {filtro_id}'''
    f'''Valor Mínimo - {filter_jogador_antigo[col_dist_jogador].min()}'''
    f'''Média - {round(filter_jogador_antigo[col_dist_jogador].mean(), 2)}'''
    f'''Mediana - {round(filter_jogador_antigo[col_dist_jogador].median(), 2)}'''
    f'''Valor Máximo - {filter_jogador_antigo[col_dist_jogador].max()}'''

    if dist_type_jogador == 'ECDF': ECDFPlot(filter_jogador_antigo, col_dist_jogador)
    else: Distplot(filter_jogador_antigo, col_dist_jogador)
with row7_2:
    f'''### Dados Após ID {filtro_id}'''
    f'''Valor Mínimo - {filter_jogador_novo[col_dist_jogador].min()}'''
    f'''Média - {round(filter_jogador_novo[col_dist_jogador].mean(), 2)}'''
    f'''Mediana - {round(filter_jogador_novo[col_dist_jogador].median(), 2)}'''
    f'''Valor Máximo - {filter_jogador_novo[col_dist_jogador].max()}'''

    if dist_type_jogador == 'ECDF': ECDFPlot(filter_jogador_novo, col_dist_jogador)
    else: Distplot(filter_jogador_novo, col_dist_jogador)

## Graficos de Correlação Jogadores -- Antes x Depois
'''## Gráficos de Correlação - Jogadores'''
row8_1,  row8_2  = st.columns(2)
with row8_1:
    f'''### Dados Antes ID {filtro_id}'''
    CorrPlot(filter_jogador_antigo, cols_corr_jogador)

with row8_2:
    f'''### Dados Após ID {filtro_id}'''
    CorrPlot(filter_jogador_novo, cols_corr_jogador)