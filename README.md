# tcc-deploy
Repositório para integração e deploy do uma intreface web em _Python + Streamlit_ como trabalho de graduação em Ciência da Computação.

# Estrutura e Conteúdo

## Arquivos de Dados

Diretórios contendo os dados de _Overview, Performance e Economy_ dos times correspondentes aos nomes destes. Arquivos em formato CSV e combinados através de funções de merge (pandas.merge) e concatenação (pandas.concat) da biblioteca **Pandas**. 

## Documentos e Imagens

A pasta [docs](https://github.com/GabrielPerson/tcc-deploy/tree/main/docs) contém o relatório da primeira parte deste trabalho de graduação - contendo as principais análises descritivas e estatísticas desenvolvidas que serviram de apoio para o desenvolvimento da interface - e o relátorio final de entrega para a conclusão do trabalho de graduação. A pasta [imgs](https://github.com/GabrielPerson/tcc-deploy/tree/main/img) contém imagens que exemplificam como os dados extraídos estão dispostos localmente na estrutura de diretórios e uma amostra da disposição dos dados de uma determinada partida no website [vlr.gg](https://www.vlr.gg).

## Código Fonte

### requirements.txt

Bibliotecas utilizadas para funcionamento e _deploy_ do código fonte da interface. Nenhuma versão específica foi utilizada.

### preprocessamento.py

Código fonte utilizado para concatenação de todos os dados presentes nos arquivos csv's, formatação e limpeza de dados inconsistentes, criação de novas variáveis e agregação de informações. Função é utilizada pela inteface para o carregamento dos dados disponíveis.

### streamlitapp.py

Código fonte principal da interface utilizando a biblioteca _[Streamlit](https://streamlit.io)_. Nesta os dados dos times são disponibilizados através de duas bases agregadas, com dados de performance individuais de jogadores e dados de performance agregada dos times, que podem ser baixadas localmente pelo usuário em arquivos CSV. A interface dispõe também de seletores para filtragem de dados em diferentes contextos e visualizações de atributos categóricos e numéricos que compõe a base.