# puc_airlines_reviews_sentiment_analysis
TCC do curso de Engenharia de Dados da PUC Minas

## Descrição
Projeto que realiza análise análise de sentimentos (Processamento de Linguagem Natural / Machine Learnig) em streaming (fluxo contínuo de dados) sobre avaliações de voos publicadas por passageiros.  
Projeto utilizado no TCC do curso de Engenharia de Dados da PUC Minas.

## Objetivo
Construção de um fluxo de processamento contínuo de mensagens postadas em diversos idiomas, onde as informações são coletadas através de APIS, tratadas e armazenadas em bancos performáticos para análise e consulta. Tais dados são trafegados em serviços de mensageria de baixa latência, processados com recursos de Machine Learning e disponibilizados para o cliente em distintos formatos de armazenamento, além de funcionalidade construída em ferramenta de Data Visualization.

## Artigo Técnico
[Artigo Técnico em formato PDF](https://github.com/fxmuld3r/puc_airlines_reviews_sentiment_analysis/blob/main/PUC%20-%20TCC%20-%20Engenharia%20de%20Dados%20-%20Andr%C3%A9%20Vieira%20de%20Lima.pdf)

## Apresentação em Vídeo
[Apresentação no YouTube (5 minutos de vídeo)](https://www.youtube.com/watch?v=KXtxDYEkhag)

## Diagrama de Arquitetura
[Arquivo em formato PNG](https://github.com/fxmuld3r/puc_airlines_reviews_sentiment_analysis/blob/main/PUC-EngenhariaDeDadosAirlineReviews.drawio.png)

## Bibliotecas Utilizadas
[Requirements.txt](https://www.youtube.com/watch?v=KXtxDYEkhag)

## Tecnologias Utilizadas
- Apache Airflow 2.1.0 (Docker);
- Apache Kafka (embutido no Apache Pinot);
- Apache Parquet;
- Apache Pinot 0.12.0;
- Apache Spark 3.4.1;
- Apache Spark Streaming 3.4.1;
- Apache Superset;
- Apache ZooKeeper (embutido no Apache Pinot);
- Docker 20.10.24;
- Flask 2.3.2;
- MongoDB (Docker);
- Python 3.10.9;
- TextBlob 0.17.1;

## Instalação
Para executar o projeto, é necessário instalar as ferramentas listadas na seção acima, conforme versões detalhadas.
___
## Arquivo de Dados com Massa de Testes
[Massa de Dados](https://github.com/fxmuld3r/puc_airlines_reviews_sentiment_analysis/tree/main/puc_airlines_reviews_sentiment_analysis/mock/data)
<br />
## Passo a Passo de Execução do Projeto
Seguem os passos para execução do projeto em ambiente Linux:
<br />
### 1) Iniciar e Configurar Ferramentas de Ingestão de Dados
#### 1.1) Iniciar Apache Pinot com Zookeper
Iniciar o Apache Pinot (o zookeper é carregado automaticamente):
```sh
~/apache-pinot-0.12.0-bin$ bin/quick-start-streaming.sh
```
A interface do Pinot pode ser acessada através do link:  http://localhost:9000

#### 1.2) Iniciar Apache Kafka no Pinot
Iniciar o Apache Kafka (com porta personalizada 9876) embutido no Apache Pinot
```sh
~/apache-pinot-0.12.0-bin$ sudo bin/pinot-admin.sh  StartKafka -zkAddress=localhost:2123/kafka -port 9876
```
#### 1.3) Incluir Schemas e Tabelas no Apache Pinot
Utilizar a [API do Pinot](http://localhost:9000/help) para incluir [Schemas do Pinot](https://github.com/fxmuld3r/puc_airlines_reviews_sentiment_analysis/blob/main/puc_airlines_reviews_sentiment_analysis/settings/schemas_pinot.txt) de dados referentes às mensagens que serão armazenadas nos tópicos Kafka 
Incluir [Realtime Tables](http://localhost:9000/#/tables) via interface web do Pinot apontadas para o broker "localhost:9876", com os seguintes nomes:
- AirlinesReviewsKafkaTopic para o tópico "airlines-reviews-kafka-topic";
- AirlinesReviewsTransformatedKafkaTopic para o tópico "airlines-reviews-transformed-kafka-topic";
- AirlinesReviewsSentimentAnalisysKafkaTopic para o tópico "airlines-reviews-sentiment-analysis-kafka-topic";
___
### 2) Ingestão de Dados
#### 2.1) Executar API de Mock de Dados de Testes (porta 5000)
Quando acionada, a API realiza a leitura de dados do arquivo de massa de dados (CSV) e aciona a API de Ingestão de Dados:
```sh
~/puc_airlines_reviews_sentiment_analysis/mock$ python3 airlines_reviews_api_data_mock.py
```
#### 2.2) Executar API de Ingestão de Avaliações de Viagens (porta 5001)
Quando acionada, a API recepciona Avaliações de Viagens e armazena (JSON) as mensagens no tópico Kafka "airlines-reviews-kafka-topic":
```sh
~/puc_airlines_reviews_sentiment_analysis/api$ python3 airlines_reviews_api_data_ingestion.py
```
#### 2.3) Executar Scheduler para Mock de Dados de Testes
O scheduler aciona a API de mock de dados, sendo que a mesma aciona a API de Ingestão:
```sh
~/puc_airlines_reviews_sentiment_analysis/mock$ python3 airlines_reviews_mock_scheduler.py
```
#### 2.4) Consultar Dados Ingeridos de Avaliações de Viagens no Apache Pinot
http://localhost:9000/#/query?query=select+*+from+AirlinesReviewsKafkaTopic+limit+10&tracing=false&useMSE=false
___
### 3) Transformação de Dados
#### 3.1) Executar Módulo Spark Streaming de Transformação de Dados
Quando acionado, o módulo realiza as seguintes ações nos textos das Avaliações de Voos (armazenando no tópico "airlines-reviews-transformed-kafka-topic"):
- Conversão do texto para letras minúsculas;
- Remoção de excessos de espaços entre as palavras;
- Remoção de quebra de linhas de parágrafos;
- Conversão do texto para o formato UTF-8;
- Remoção de URLs nos textos;
- Tradução das mensagens dos idiomas originais (português, espanhol, italiano, francês, árabe, alemão, chinês, turco, indiano, holandês, japonês e grego) para o idioma inglês através da API
pública do Google Translate.
```sh
~/puc_airlines_reviews_sentiment_analysis/streaming$ python3 airlines_reviews_streaming_transformation.py
```
#### 3.2) Consultar Avaliações de Voos Transformadas no Apache Pinot
http://localhost:9000/#/query?query=select+*+from+AirlinesReviewsTransformatedKafkaTopic+limit+10&tracing=false&useMSE=false
___
### 4) Análise de Sentimento (Machine Learning)
#### 4.1) Executar Módulo Spark Streaming para Análise de Sentimentos das Avaliações de Voos
Quando acionado, o módulo realiza o processamento de linguagem natural através de processo de Machine Learning. O resultado com análise de polaridade e subjetividade são armazenandos no tópico "airlines-reviews-sentiment-analysis-kafka-topic" em formato JSON:
```sh
~/puc_airlines_reviews_sentiment_analysis/streaming$ python3 airlines_reviews_streaming_sentiment_analysis.py
```
#### 4.2) Consultar Análise de Sentimentos em Avaliações de Voos no Apache Pinot
http://localhost:9000/#/query?query=select+*+from+AirlinesReviewsSentimentAnalisysKafkaTopic+limit+10&tracing=false&useMSE=false
___
### 5) Armazenamento de Avaliações Negativas de Voos em Banco de Dados NOSQL
#### 5.1) Executar MongoDB no Docker
```sh
sudo docker start <numero processo MongoDB>
```
#### 5.2) Executar Módulo Spark Streaming que consome dados de Análise de Sentimentos das Avaliações de Voos e Armazena em Banco NOSQL
Quando acionado, o módulo consome os dados do tópico Kafka "airlines-reviews-sentiment-analysis-kafka-topic", filtra avaliações negativas e armazena em fluxo contínuo as mensagens no formato JSON no MongoDB:
```sh
~/puc_airlines_reviews_sentiment_analysis/streaming$ python3 airlines_reviews_streaming_sentiment_analysis_ingestion.py
```
#### 5.3) Consultar Análise Avaliações Negativas no MongoDB
Utilizar Studio 3T ou similar (client MongoDB) para consultar mensagens negativas armazenadas.
___
### 6) Disponibilizar Avaliações Negativas de Voos em API
Iniciar API que fornece dados de Avaliações Negativas:
```sh
~/puc_airlines_reviews_sentiment_analysis/api$ python3 airlines_reviews_negatives_api.py
```
Consultar API com avaliações negativas (porta 5002), como exemplos:
- http://127.0.0.1:5002/negatives-reviews?selected_airline=TurkishFly
- http://127.0.0.1:5002/negatives-reviews?selected_airline=TurkishFly&fligth_date=2022-07-25
- http://127.0.0.1:5002/negatives-reviews?selected_airline=TurkishFly&flight_date=2022-07-25
___
### 7) Visualizar Avaliações Negativas de Voos em Dashboard via Apache Superset
#### 7.1) Iniciar o Apache Superset
```sh
~/Superset$export FLASK_APP=superset
~/Superset$export SUPERSET_SECRET_KEY="?????"
~/Superset$superset db upgrade
~/Superset$superset run -p 8088 --with-threads --reload --debugger
Configure a chama ao Pinot: pinot+http://localhost:8000/query?server=http://localhost:9000/
```
#### 7.2) Consultar Estatísticas de Avaliações em Dashboad no Apache Superset
Acione o endereço da aplicação:
```sh
http://localhost:8088/superset/welcome/
```
Elabore Dashboards com gráficos sob demanda
___
### 8) Extração de Avaliações de Vôos para arquivo no Formato Parquet
Iniciar o Apache Airflow para agendamento de processos:
```sh
airflow webserver -p 8080
airflow schedule
http://localhost:8080/home
```
Acionar serviço agendado através do arquivo ([dag_airlines_reviews_batch_extraction_sentiment_analysis.py](https://github.com/fxmuld3r/puc_airlines_reviews_sentiment_analysis/blob/main/dag_airlines_reviews_batch_extraction_sentiment_analysis.py)) de DAG criado.
<br />
