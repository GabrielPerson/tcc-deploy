'''
FUNCIONALIDADES DA APLICAÇÃO

- VISUALIAÇÕES
    . estatísticas (min, max, med, mean)

- FILTROS

- INTERAÇÕES
    . download de gráficos -- DIFICIL

'''
from email.policy import default
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessamento import Preproc

pd.options.display.float_format = '{:.2f}'.format

@st.cache
def Format(df, style_dict):
    return df.reset_index(drop=True).style.format(style_dict)

def FilterJogadores(df, id, times, agentes, mapas, resultado):

    if len(times) > 0: df = df[df['Time'].isin(times)]
    if len(agentes) > 0: df = df[df['Agente'].isin(agentes)]
    if len(mapas) > 0: df = df[df['Mapa'].isin(mapas)]
    if resultado != 'Ambos': df = df.loc[df.Resultado == resultado]
    df_antes = df[df['ID Partida'] <= id]
    df_depois = df[df['ID Partida'] >= id]

    return df_antes.reset_index(drop=True), df_depois.reset_index(drop=True)

def FilterTimes(df, id, times, mapas, resultado):

    if len(times) > 0: df = df[df['Time'].isin(times)]
    if len(mapas) > 0: df = df[df['Mapa'].isin(mapas)]
    if resultado != 'Ambos': df = df.loc[df.Resultado == resultado]
    df_antes = df[df['ID Partida'] <= id]
    df_depois = df[df['ID Partida'] >= id]


    return df_antes.reset_index(drop=True), df_depois.reset_index(drop=True)

def ScatterPlot(df, col):

    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': '#0e1117',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 9,
          'axes.labelsize': 12,
          'xtick.labelsize': 9,
          'ytick.labelsize': 14}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=df.index, y=df[col], color='#f94555')
    #plt.xlabel('Valor')
    plt.ylabel(col)
    plt.title(f'Gráfico Dispersão de {col}')
    st.pyplot(fig)

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
    #plt.axvline(df[col].mean(), 0,0.5, color='white')
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
          'font.size' : 14,
          'axes.labelsize': 12,
          'xtick.labelsize': 9,
          'ytick.labelsize': 14}
    
    plt.rcParams.update(rc)

    ax = sns.heatmap(corr_spearman,  fmt=".3f", vmin=0, vmax=1, mask=mask,  annot=True)
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
TITLE = "Interface Web de visualização de estatísticas do cenário competitivo brasileiro de VALORANT"

st.set_page_config(page_title=TITLE,layout='wide')
st.markdown(f'''# {TITLE}&#x2122''')

with st.expander("Introdução"):
    '''
    ## Resumo

    O trabalho desenvolvido tem como objetivo aplicar métodos de ciências de dados para extração, processamento e análise de dados no âmbito de esportes eletrônicos, especificamente sobre dados de partidas competitivas de times brasileiros de Valorant. 
    Na última década o mercado de e-sports tem crescido ano após ano, tanto em termos de receita e [premiações de campeonatos](https://liquipedia.net/valorant/Portal:Statistics) como em adesão de público em arenas, plataformas de streaming e redes sociais. 
    Grandes organizações tem adotado a cultura data driven e o uso de dados no direcionamento de decisões e estratégias para a evolução no cenário
    competitivo. 
    A metodologia do trabalho consiste na extração e armazenamento local de dados web de partidas competitivas, pré-processamento dos conjuntos de dados e aplicação
    de técnicas de análises descritivas para avaliação das principais métricas de performance de times e jogadores. 
    Os métodos de análise aplicados permitiram adquirir um melhor conhecimento sobre a natureza dos dados utilizados, quantificar relações entre
    atributos numéricos e categóricos e identificar diferenças significativas entre perfis de
    combate de jogadores. Os resultados encontrados estão divulgados através de tabelas e diferentes visualizações em uma interface web interativa disponível [neste link](https://share.streamlit.io/gabrielperson/tcc-deploy/main/streamlitapp.py). 

    ## Contextualização

    Na ultima década  a indústria de Jogos Digitais e *E-Sports* tem crescido ano após ano tanto em termos de receita como de jogadores/espectadores, com mais organizações e grandes marcas investindo no mercado e pessoas consumindo mais produtos e assistindo mais campeonatos através de plataformas de *streaming*. 
    Aliado ao crescimento desta indústria tem-se a disseminação da cultura [*Data Driven*](https://neilpatel.com/br/blog/data-driven) em diversas outras indústrias no mundo todo, onde decisões de negócio são direcionadas e tomadas baseando-se em estudos e análise de dados e indicadores e não somente em suposições, inferências e experiências.

    No meio dos _E-Sports_ esta cultura se estabeleceu através de organizações e times investindo na capacitação de jogadores e comissão técnica, principalmente através de [técnicos e analistas que valorizam e utilizam dados](https://www.hltv.org/news/28332/valens-joins-evil-geniuses-as-head-of-data-science) em tomadas de decisão e estratégias e a adoção de plataformas como [shadow.gg](https://shadow.gg) e [mobalytics.gg](https://mobalytics.gg) que utilizam dos dados gerados pelo próprios jogadores em partidas para gerar análises das principais métricas de performance auxiliando os jogadores no estudo de adversários, adoção das melhores estratégias e minimização de falhas.

    O desenvolvimento dessa interface se motiva nos métodos de análises de dados utilizados por essas plataformas e demais aplicações de ciências de dados e na importância de sua utilização e divulgação à comunidade para a evolução dos _E-Sports_ em alto nível.

    ## Objetivos

    ### Obetivos Gerais:

    O trabalho desenvolvido ao longo do POC I e POC II (Projeto Orientado a Computação) tem como objetivo a aplicação de técnicas de mineração de dados e [KDD (Knowledge Discovery in Data)](https://pt.wikipedia.org/wiki/Extração_de_conhecimento) sobre os dados de partidas de times brasileiros disponíveis publicamente no website [www.vlr.gg](https://www.vlr.gg), 
    desenvolvimento de análises exploratórias e estatísticas sobre os dados coletados e a divulgação dos principais resultados e métricas de performance em uma interface web disponível à toda comunidade. O relatório desenvolvido e divulgado como entrega do POC I pode ser encontrado na pasta 'docs' disponível no repositório github deste projeto e baixado [aqui.](https://github.com/GabrielPerson/tcc-deploy/raw/main/docs/POC%201%20-%20GABRIEL%20PERSON.pdf)

    ### Objetivos Específicos:

    - Extração dos dados através de técnicas de [Web Scraping](https://pt.wikipedia.org/wiki/Coleta_de_dados_web) e armazenamento em arquivos locais.

    - Avaliação de métricas de performance inerentes ao jogo através de técnicas de análises descritivas e estatísticas.

    - Desenvolvimento de uma interface web para a divulgação dos dados, análises e visualizações desenvolvidas para a comunidade brasileira e internacional.

    '''

with st.expander("Metodologia"):
    '''
    ## Fonte de Dados

    Os dados utilizados no desenvolvimento do trabalho foram extraídos do website [www.vlr.gg](https://www.vlr.gg) considerado um dos maiores portais de divulgação de conteúdo e resultados do cenário competitivo de Valorant mundial, disponibilizando resultados
    de partidas, estatísticas de times e jogadores, ranqueamento de times por cada região de
    disputa, fóruns de discussão e notícias recentes sobre times e jogadores. 

    _Disclaimer_: Os dados utilizados estão sujeitos à qualidade e disponibilidade destes no próprio website. 


    ## Extração e Armazenamento dos Dados

    Para a extração dos dados de cada partida são utilizadas as bibliotecas [Urllib](https://docs.python.org/3/howto/urllib2.html), [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc) e [Pandas](https://pandas.pydata.org/pandas-docs/stable/index.html), onde cada página de interesse é acessada através de uma URL (Uniform Resource Locator)
    específica para cada série de partidas disputadas entre dois times e para cada partida são
    extraídos dados de interesse das abas [Overview](https://www.vlr.gg/51296/acend-vs-gambit-esports-valorant-champions-2021-gf/?game=57981&tab=overview), [Performance](https://www.vlr.gg/51296/acend-vs-gambit-esports-valorant-champions-2021-gf/?game=57981&tab=performance) e [Economy](https://www.vlr.gg/51296/acend-vs-gambit-esports-valorant-champions-2021-gf/?game=57981&tab=economy), previamente
    nomeadas pelos criadores do portal. A figura abaixo exemplifica como os dados são dispostos
    na aba __Overview__.

    ![Página Overview](https://github.com/GabrielPerson/tcc-deploy/blob/main/img/overviw_vlr.png?raw=true)


    As informações de desempenho dos jogadores para a série e cada mapa dispostas em
    formato de tabelas _html_ são extraídas utilizando-se a função **read_html** da biblioteca
    Pandas, que identifica automaticamente os dados dessas tabelas e armazena em estruturas
    do tipo **Dataframes** no ambiente de execução. As demais informações dispostas na página,
    como rodadas vencidas por cada time, mapas disputados, versão do jogo e agentes utilizados
    são acessados e extraídos através de suas respectivas tags *html* e armazenados em listas e
    variáveis de ambiente.

    Os dados brutos extraídos passsam por uma etapa de pré-processamento para o tratamento de valores nulos, conversão de valores e criação de novos atributos para serem armazenados em arquivos do tipo _csv (comma separated value)_. Os dados comportam as partidas oficiais e indexadas pelo **vlr.gg** dos principais times brasileiros a partir do mês de Setembro de 2020. Embora existam partidas oficiais datadas
    de desde Junho de 2020, mês do lançamento oficial de Valorant , essas partidas não
    possuem informações suficientes disponíveis no website, portanto foram desconsideradas.

    ## Análise de Dados

    O processo de análises exploratórias e estatísticas foi
    conduzido com a intenção de prover melhores visualizações e conhecimento sobre os dados
    utilizados no desenvolvimento do trabalho, através de correlações de atributos, quantidades
    absoluta de ocorrências de valores, estatísticas descritivas - média, mediana, quartis, etc... - e distribuição dos dados

    As análises foram conduzidas utilizando-se funções disponíveis nas bibliotecas Pandas, [Scipy](https://docs.scipy.org/doc/scipy/reference/index.html) e [Seaborn](https://seaborn.pydata.org/index.html), sendo as primeiras utilizdas em manipulações e análises
    descritivas e a última na geração de gráficos para visualização dos dados
    em diferentes contextos, como gráficos de dispersão, densidade, quantidade, distribuição e correlação dos dados

    O repositório github contendo a maior parte do código utilizado na extração dos dados e desenvolvimento das análises se encontra [neste link](https://github.com/GabrielPerson/vlrgg-analytics)

    ## Interface Wenb

    Esta interface web foi desenvolvida com o propósito de divulgar as análises e estudos desenvolvidos sobre a base de dados extraida. Após pesquisas sobre os principais _framworks_ Python de desenvolvimento web (Django, Flask, etc...), foi escolhido o **[Streamlit](https://streamlit.io)**, principalmente por ser muito utilizado no desenvolvimento de aplicativos voltados para a divulgação de trablalhos sobre dados. Sua simplicidade e robustez possibilitou a migração de funções já desenvolvidas anteriormente no curso do trabalho para tratamento e visualização dos dados.

    O suporte do _framework_ à linguagem **Markdown** facilita a escrita de textos explicativos sobre o trabalho que visam o melhor entendimento do usuário. Tem-se o também o suporte a diversas ferramentas de divulgação de interação do usuário com os dados e visualizações disponíveis, como visualização e _download_ de tabelas de dados e filtros de seleções de valores (multiseletores, _sliders_), podendo ser facilmente incluídos na interface, não necessitando de um grande conhecimento e de linguagens específicas de desenvolvimento web como _JavaScript_, além de tornar a experiência do usuário muito mais completa e interativa.


    '''

with st.expander("Resultados"):

    f'''
    ## Base de Dados

    Um dos principais resultados alcançados no desenvolvimento do trabalho foi a estruturação de uma base de dados extraídos do website [www.vlr.gg](https://www.vlr.gg) composta pelas partidas disputadas pelos principais times brasileiros de Valorant, uma vez que não há a possibilidade de se obter esses dados diretamente com a desenvolvedora Riot Games através de uma API pública.

    Desde o ínicio do desenvolvimento do trabalho a base de dados tem sido constatemente atualizada com as partidas dos principais times do país a partir de Setembro de 2020 e atualmente é composta por diretórios separados por times - como ilustrado abaixo - e por conjuntos de dados gerais de times e jogadores, combinados de todos os arquivos, estes contendo respectivamente {df_times.shape[0]} e {df_jogadores.shape[0]} linhas atualmente.

    ![Dretório Local de Arquivos](https://github.com/GabrielPerson/tcc-deploy/blob/main/img/files_csv.png?raw=true)

    ![Arquivos Gamelanders](https://github.com/GabrielPerson/tcc-deploy/blob/main/img/gl_files.png?raw=true)

    ## Interface Web

    Como extensão do trabalho realizado do POC I foi desenvolvida esta interface web para a divulgação não somente do conjunto de dados utilizado mas também das principais análises desenvolvidas sobre os diversos atributos presentes nas bases.

    A priorização do desenvolvimento de uma interface web de fácil divulgação e acessibilidade sobre o desenvolvimento de um artigo visa promover a acessibilidade e interação da comunidade de Valorant - jogadores casuais, profissionais, técnicos, analistas e criadores de conteúdo - com toda a informação e conhecimento desenvolvido sobre os dados e análises. Esta com o principal objetivo que as informações divulgadas possam contribuir para a evolução técnica e tática do cenário competitivo e na conquista de diversos títulos internacionais juntamente aos jogadores brasileiros vitoriosos em diversos outros jogos competitivos.

    '''

with st.expander("Conclusão"):
    
    '''
    ## Principais Desafios

    Todo este trabalho desenvolvido começou com um lapso de curiosidade de um intusiasta de dados e ávido jogador de Valorant sobre a viabilidade de obtenção e análises de dados de partidas competitivas. Desde então a principal dificuldade encontrada no decorrer do desenvolvimento foi a acessibilidade dos mais diversos dados disponíveis online, seja por páginas com dados incompletos ou pela inerente dificuldade de obtenção de dados através de métodos de Web Scraping, onde muitas das informações devem ser obtidas através do acesso de tags HTML muito específicas em uma página pondendo levar a diversas inconsitências através das centenas de páginas que devem ser acessadas e mineradas.

    Grande parte dessa principal dificuldade foi mitigada por experiência prévia em aplicação de técnicas de Web Scaraping em demais projetos de pesquisa densvolvidos ao longo da graduação e pelo fácil acesso a parte dos dados presentes em tabelas HTML através de funções da biblioteca Pandas após uma sucinta análise da estrtura e distribuição das principais informações no website.

    ## Evolução do Trabalho

    O trabalho desenvolvido até aqui pode ser evoluido em diversos aspectos, sendo o principal deles a viabilidade da extração de milhares de partidas competitivas das diversas regiões do mundo, uma vez que as páginas contendo as informações de cada partida podem ser acessadas através de links no formato "http://vlr.gg/<id_partida>", porém sendo necessárias alterações nos códigos responsáveis pelo acesso e extração dos dados para a identificação  e mitigação de diversas inconsistencias que possam surgir.

    Ao ser possível o acesso e extração de dezenas de milhares de partidas competitivas essas informações podem ser armazenadas publicamente em bancos de dados de serviços de nuvem, possibilitando o fácil e rápido acesso por praticamente todos os entusiastas de Valorant para o desenvolvimento de diversas soluções baseadas em dados e futuros estudos.

    As referências utilizadas para o desenvolvimento deste trabalho se encontram disponíveis através de _hiperlinks_ na documentação 
    referentes a métodos, bibliotecas utilizadas e fontes externas de informação

    '''

'''---'''

##QUAIS FILTROS EU QUERO PARA OS DADOS

## Sidebar -----------------------
st.sidebar.markdown(
''' ## Filtros de Dados

Os filtros a seguir podem ser utilizados para selecionar Partidas, Mapas, Times, ou Agentes específicos para se gerar um conjunto
de dados específico para uma análise mais direcionada. 

Como não foi possível extrair a data exata de cada partida o "Match ID" é utilizado
como filtro temporal, partidas no ano de 2020 possuem um ID menor que 7000.

A página de uma partida de um determinado ID pode ser acessado através do link www.vlr.gg/<id partida> 

(Ex: https://www.vlr.gg/10268)
'''
)

filtro_times = st.sidebar.multiselect('Filtro de Times', TIMES)
filtro_agentes = st.sidebar.multiselect('Filtro de Agentes - Somente dados Jogadores', AGENTES)
filtro_mapas = st.sidebar.multiselect('Filtro de Mapas', MAPAS)
filtro_result = st.sidebar.selectbox('Resultado', ['Vitoria', 'Derrota', 'Ambos'], index=2)
filtro_id = st.sidebar.select_slider('Filtro de Partidas por ID',  options=df_times['ID Partida'].unique(), value=8228)


st.sidebar.markdown(''' --- 
## Filtros dos gráficos de Times ''')
col_count_time = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Quantidade - Times', options = df_times.select_dtypes(include=['object']).columns, index=1)
col_dist_time = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Distribuição - Times', options = df_times.select_dtypes(exclude=['object']).columns, index=1)
cols_corr_time = st.sidebar.multiselect('Seleciona as colunas para o gráfico de Correlação - Times', options = df_times.columns, default=['Win Rate', 'Win Rate ATK', 'Win Rate DEF'])
num_obj = st.sidebar.slider('Quantidade de valores do gráfico de Quantidade - Times', min_value=1, max_value=20, value=20)

st.sidebar.markdown(''' --- 
## Filtros dos gráficos de Jogadores ''')
col_count_jogador = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Quantidade - Jogadores', options = df_jogadores.select_dtypes(include=['object']).columns, index=1)
col_dist_jogador = st.sidebar.selectbox('Selecione a coluna para apresentar no gráfico de Distribuição - Jogadores', options = df_jogadores.select_dtypes(exclude=['object']).columns)
cols_corr_jogador = st.sidebar.multiselect('Seleciona as colunas para o gráfico de Correlação - Jogadores', options = df_jogadores.columns, default=['ACS', 'First Kill Por Round', 'First Death Por Round'])

## -------------------------------

## Amostra das bases'
'''## Amostras de Dados'''
'''Uma breve amostra dos dados utilizados no desenvolvimento das análises e visuallizações disponíveis na interface. 
Dados dos times são compostos por somas e médias dos dados dos jogadores deste para uma determinada partida.'''


style_dict_times={
    'ACS':'{:.0f}',
    'Kills':'{:.0f}', 'Deaths':'{:.0f}', 'Assists':'{:.0f}', 'Diferenca Kill/Death':'{:.0f}',
    'ADR':'{:.2f}','HS%':'{:.0f}','Nota Economia':'{:.1f}','First Kills':'{:.0f}','First Deaths':'{:.0f}','Kills Por Round':'{:.2f}',
    'Deaths Por Round':'{:.2f}','Assists Por Round':'{:.2f}','First Kill Por Round':'{:.2f}','First Death Por Round':'{:.2f}','Double Kills':'{:.0f}',
    'Triple Kills':'{:.0f}','Quadra Kills':'{:.0f}','Penta Kills':'{:.0f}','1v1':'{:.0f}', '1v2':'{:.0f}', '1v3':'{:.0f}', '1v4':'{:.0f}', '1v5':'{:.0f}', 
    'Plants':'{:.0f}','Defuses':'{:.0f}','Total Mult Kills':'{:.0f}','Mult Kills Por Round':'{:.2f}','Total Clutches':'{:.0f}','Clutches Por Round':'{:.2f}','Rounds Vencidos':'{:.0f}',
    'Rounds Perdidos':'{:.0f}','Vitorias DEF':'{:.0f}', 'Derrotas DEF':'{:.0f}', 'Vitorias ATK':'{:.0f}', 'Derrotas ATK':'{:.0f}', 'Vitorias Pistol':'{:.0f}',
    'Total Pistol':'{:.0f}','Win Rate Pistol':'{:.0f}','Total Eco':'{:.0f}','Vitorias Eco':'{:.0f}','Win Rate Eco':'{:.0f}',
    'Total Semi Eco':'{:.0f}','Vitorias Semi Eco':'{:.0f}','Win Rate Semi Eco':'{:.0f}','Total Semi Buy':'{:.0f}','Vitorias Semi Buy':'{:.0f}',
    'Win Rate Semi Buy':'{:.0f}','Total Full Buy':'{:.0f}','Vitorias Full Buy':'{:.0f}','Win Rate Full Buy':'{:.0f}','Score Comp Agro':'{:.0f}',
    'Score Comp Tempo':'{:.0f}','Score Comp Control':'{:.0f}','Score Comp Agro Oponente':'{:.0f}','Score Comp Tempo Oponente':'{:.0f}',
    'Score Comp Control Oponente':'{:.0f}', 'Rounds Totais':'{:.0f}', 'Win Rate':'{:.2f}', 'Win Rate DEF':'{:.2f}', 'Win Rate ATK':'{:.2f}'
}

style_dict_jogadores={
    'ACS':'{:.0f}',
    'Kills':'{:.0f}', 'Deaths':'{:.0f}', 'Assists':'{:.0f}', 'Diferenca Kill/Death':'{:.0f}',
    'ADR':'{:.2f}','HS%':'{:.0f}','Nota Economia':'{:.1f}','First Kills':'{:.0f}','First Deaths':'{:.0f}','Diferenca FK/FD':'{:.0f}','Kills Por Round':'{:.2f}','Deaths Por Round':'{:.2f}',
    'Assists Por Round':'{:.2f}','First Kill Por Round':'{:.2f}','First Death Por Round':'{:.2f}','Double Kills':'{:.0f}','Win Rate First Kills':'{:.0f}',
    'Triple Kills':'{:.0f}','Quadra Kills':'{:.0f}','Penta Kills':'{:.0f}','1v1':'{:.0f}', '1v2':'{:.0f}', '1v3':'{:.0f}', '1v4':'{:.0f}', '1v5':'{:.0f}', 
    'Plants':'{:.0f}','Defuses':'{:.0f}','Total Mult Kills':'{:.0f}','Mult Kills Por Round':'{:.2f}','Total Clutches':'{:.0f}','Clutches Por Round':'{:.2f}'
}

''' ### Dados de Times '''
st.dataframe(Format(df_times.sample(20, replace=True), style_dict_times))
#st.write(df_times.sample(20, replace=True))
DownloadCSV(DfToCSV(df_times), 
            'Baixar Conjunto de Dados de Jogadores',
            'jogadores.csv')

''' ### Dados de Jogadores'''
#st.dataframe(df_jogadores.sample(20, replace=True))
st.dataframe(Format(df_jogadores.sample(20, replace=True), style_dict_jogadores))
DownloadCSV(DfToCSV(df_jogadores), 
            'Baixar Conjunto de Dados de Times',
            'times.csv')

st.markdown('''---''')

## Dados Times Filtrados
'''## Dados Filtrados Times

As tabelas a seguir são amostras filtradas da base original de acordo com os valores escolhidos na barra lateral e são utilizdas na criação dos gráficos abaixo.

Podem ser baixadas em formato *csv* através do botão "**Baixar Dados Filtrados**"
'''

row2_1, row2_2 = st.columns(2)
filter_times_antigo, filter_times_novo = FilterTimes(df_times, filtro_id, filtro_times, filtro_mapas, filtro_result)
#vitorias_filtrado_antigo = filter_times_antigo[filter_times_antigo.Resultado == 'Vitoria']
#vitorias_filtrado_novo  = filter_times_novo[filter_times_novo.Resultado == 'Vitoria']

with row2_1:
    f'''### Times - Antes ID {filtro_id}'''
    st.write(f'Total de Linhas - {filter_times_antigo.shape[0]}')
    st.dataframe(filter_times_antigo.style.format(style_dict_times))
    DownloadCSV(DfToCSV(filter_times_antigo), 
                'Baixar Dados Filtrados',
                'times_filtrados_antesID.csv')
with row2_2:
    f'''### Times - Depois ID {filtro_id}'''
    st.write(f'Total de Linhas - {filter_times_novo.shape[0]}')
    st.dataframe(filter_times_novo.style.format(style_dict_times))
    DownloadCSV(DfToCSV(filter_times_novo), 
                'Baixar Dados Filtrados',
                'times_filtrados_depoisID.csv')


## Graficos de Contagem Times -- Antes x Depois
'''
## Gráficos de Quantidade - Times
São utilizados para se comparar quantidades absolutas entre diferentes valores de um atributo. Por exemplo querendo-se comparar a quantidade de mapas disputados por um determinado time ou 
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

Dentre as opções disponíveis - ECDF, Histograma e Dispersão - tem-se o gráfico de distribuição cumulativa 
([ECDF](https://towardsdatascience.com/what-why-and-how-to-read-empirical-cdf-123e2b922480 "ECDF - Towards Data Sciente")) 
para se observar para qual valor X temos até Y das observaços da amostra, 
o Histograma, apresentando faixas de agrupamentos de valores onde quanto maior a faixa mais valores temos dentro desta
e o gráfico de dispersão (_Scatterplot_) que apresenta como os pontos de dados se distribuem no espaço.

Juntamente aos gráficos tem-se também métricas importantes sobre o atributo analisado, como valor mínimo, média, mediana e máximo, assim como qual time
obteve os respectivos valores extremos e em qual mapa isso ocorreu.
'''
dist_type_time = st.radio("", options=['ECDF - Ditribuição Cumulativa', 'Histograma'])
row4_1, row4_2  = st.columns(2)
with row4_1:
    f'''### Dados Antes ID {filtro_id}'''
    f'''{col_dist_time} Mínimo — {filter_times_antigo[col_dist_time].min()}
        — Time: {filter_times_antigo.at[filter_times_antigo[col_dist_time].idxmin(), 'Time']}
        — Mapa: {filter_times_antigo.at[filter_times_antigo[col_dist_time].idxmin(), 'Mapa']}'''
    f'''{col_dist_time} Médio — {round(filter_times_antigo[col_dist_time].mean(), 2)}'''
    f'''Mediana — {round(filter_times_antigo[col_dist_time].median(), 2)}'''
    f'''{col_dist_time} Máximo — {filter_times_antigo[col_dist_time].max()}
        — Time: {filter_times_antigo.at[filter_times_antigo[col_dist_time].idxmax(), 'Time']}
        — Mapa: {filter_times_antigo.at[filter_times_antigo[col_dist_time].idxmax(), 'Mapa']}'''

    if dist_type_time == 'ECDF - Ditribuição Cumulativa': ECDFPlot(filter_times_antigo, col_dist_time)
    else: Distplot(filter_times_antigo, col_dist_time)
    ScatterPlot(filter_times_antigo, col_dist_time)
with row4_2:
    f'''### Dados Após ID {filtro_id}'''
    f'''{col_dist_time} Mínimo — {filter_times_novo[col_dist_time].min()}
        — Time: {filter_times_novo.at[filter_times_novo[col_dist_time].idxmin(), 'Time']}
        — Mapa: {filter_times_novo.at[filter_times_novo[col_dist_time].idxmin(), 'Mapa']}'''
    f'''{col_dist_time} Médio — {round(filter_times_novo[col_dist_time].mean(), 2)}'''
    f'''Mediana — {round(filter_times_novo[col_dist_time].median(), 2)}'''
    f'''{col_dist_time} Máximo — {filter_times_novo[col_dist_time].max()}
        — Time: {filter_times_novo.at[filter_times_novo[col_dist_time].idxmax(), 'Time']}
        — Mapa: {filter_times_novo.at[filter_times_novo[col_dist_time].idxmax(), 'Mapa']}'''

    if dist_type_time == 'ECDF - Ditribuição Cumulativa': ECDFPlot(filter_times_novo, col_dist_time)
    else: Distplot(filter_times_novo, col_dist_time)
    ScatterPlot(filter_times_novo, col_dist_time)

'''
## Gráficos de Correlação - Times

Utilizados para apresentar o cálulo da correlação linear de [Pearson](https://towardsdatascience.com/clearly-explained-pearson-v-s-spearman-correlation-coefficient-ada2f473b8 "Correlação de Spearman - Towards Data Science"),
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
filter_jogador_antigo, filter_jogador_novo = FilterJogadores(df_jogadores, filtro_id, filtro_times, filtro_agentes, filtro_mapas, filtro_result)

## Dados Jogadores Filtrados
'''## Dados Filtrados Jogadores

As tabelas a seguir são amostras filtradas da base original de acordo com os valores escolhidos na barra lateral e são utilizdas na criação dos gráficos abaixo.

Podem ser baixadas em formato *csv* através do botão "**Baixar Dados Filtrados**"
'''
row5_1,  row5_2  = st.columns(2)
with row5_1:
    f'''### Antes ID {filtro_id}'''
    st.write(f'Total de Linhas - {filter_jogador_antigo.shape[0]}')
    st.dataframe(filter_jogador_antigo.style.format(style_dict_jogadores))
    DownloadCSV(DfToCSV(filter_jogador_antigo), 
                'Baixar Dados Filtrados',
                'jogadores_filtrados_antesID.csv')
with row5_2:
    f'''### Depois ID {filtro_id}'''
    st.write(f'Total de Linhas - {filter_jogador_novo.shape[0]}')
    st.dataframe(filter_jogador_novo.style.format(style_dict_jogadores))
    DownloadCSV(DfToCSV(filter_jogador_novo), 
                'Baixar Dados Filtrados',
                'jogadores_filtrados_depoisID.csv')


'''## Gráficos de Quantidade - Jogadores'''
row6_1,  row6_2  = st.columns(2)
## Graficos de Contagem Times -- Antes x Depois
with row6_1:
    f'''### Dados Antes ID {filtro_id}'''
    Countplot(filter_jogador_antigo, col_count_jogador, num_obj)
with row6_2:
    f'''### Dados Após ID {filtro_id}'''
    Countplot(filter_jogador_novo, col_count_jogador, num_obj)


## Graficos de Contagem Jogadores -- Antes x Depois
'''## Gráficos de Distribuição - Jogadores

Os gráficos de dispersão dos dados de jogadores seguem a mesma lógica dos gráficos dos dados de times, porém apresentando visualizações e métricas
de estatísticas individuais, assim como quais jogadores com quais agentes obtiveram valores extremos.
'''
dist_type_jogador = st.radio("", options=['ECDF', 'Histograma'])
row7_1,  row7_2  = st.columns(2)
with row7_1:
    f'''### Dados Antes ID {filtro_id}'''
    f'''{col_dist_jogador} Mínimo — {filter_jogador_antigo[col_dist_jogador].min()}
        — Jogador: {filter_jogador_antigo.at[filter_jogador_antigo[col_dist_jogador].idxmin(), 'Jogador']}
        — Agente: {filter_jogador_antigo.at[filter_jogador_antigo[col_dist_jogador].idxmin(), 'Agente']}'''
    f'''{col_dist_jogador} Médio — {round(filter_jogador_antigo[col_dist_jogador].mean(), 2)}'''
    f'''Mediana - {round(filter_jogador_antigo[col_dist_jogador].median(), 2)}'''
    f'''{col_dist_jogador} Máximo — {filter_jogador_antigo[col_dist_jogador].max()}
        — Jogador: {filter_jogador_antigo.at[filter_jogador_antigo[col_dist_jogador].idxmax(), 'Jogador']}
        — Agente: {filter_jogador_antigo.at[filter_jogador_antigo[col_dist_jogador].idxmax(), 'Agente']}'''

    if dist_type_jogador == 'ECDF': ECDFPlot(filter_jogador_antigo, col_dist_jogador)
    else: Distplot(filter_jogador_antigo, col_dist_jogador)
    ScatterPlot(filter_jogador_antigo, col_dist_jogador)

with row7_2:
    f'''### Dados Após ID {filtro_id}'''
    f'''{col_dist_jogador} Mínimo — {filter_jogador_novo[col_dist_jogador].min()}
        — Jogador: {filter_jogador_novo.at[filter_jogador_novo[col_dist_jogador].idxmin(), 'Jogador']}
        — Agente: {filter_jogador_novo.at[filter_jogador_novo[col_dist_jogador].idxmin(), 'Agente']}'''
    f'''{col_dist_jogador} Médio — {round(filter_jogador_novo[col_dist_jogador].mean(), 2)}'''
    f'''Mediana - {round(filter_jogador_novo[col_dist_jogador].median(), 2)}'''
    f'''{col_dist_jogador} Máximo — {filter_jogador_novo[col_dist_jogador].max()}
        — Jogador: {filter_jogador_novo.at[filter_jogador_novo[col_dist_jogador].idxmax(), 'Jogador']}
        — Agente: {filter_jogador_novo.at[filter_jogador_novo[col_dist_jogador].idxmax(), 'Agente']}'''

    if dist_type_jogador == 'ECDF': ECDFPlot(filter_jogador_novo, col_dist_jogador)
    else: Distplot(filter_jogador_novo, col_dist_jogador)
    ScatterPlot(filter_jogador_novo, col_dist_jogador)

## Graficos de Correlação Jogadores -- Antes x Depois
'''## Gráficos de Correlação - Jogadores

Os gráficos de correlação dos dados de jogadores seguem a mesma lógica dos gráficos dos dados de times, porém apresentado os valores do teste de correlação
de Pearson entre as estaísticas individuais dos jogadores e como elas se correlacionam.
'''
row8_1,  row8_2  = st.columns(2)
with row8_1:
    f'''### Dados Antes ID {filtro_id}'''
    CorrPlot(filter_jogador_antigo, cols_corr_jogador)
with row8_2:
    f'''### Dados Após ID {filtro_id}'''
    CorrPlot(filter_jogador_novo, cols_corr_jogador)