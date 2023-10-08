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

## Arquivo de Dados com Massa de Testes
[Massa de Dados](https://github.com/fxmuld3r/puc_airlines_reviews_sentiment_analysis/tree/main/puc_airlines_reviews_sentiment_analysis/mock/data)

## Passo a Passo de Execução do Projeto

### 1) Apache Pinot com Zookeper
Iniciar o Apache Pinot (o zookeper é carregado automaticamente):
```sh
~/apache-pinot-0.12.0-bin$ bin/quick-start-streaming.sh
```
A interface do Pinot pode ser acessa através do link:  http://localhost:9000

### 2) Apache Kafka no Pinot
Iniciar o Apache Kafka (com porta personalizada 9876) embutido no Apache Pinot
```sh
~/apache-pinot-0.12.0-bin$ sudo bin/pinot-admin.sh  StartKafka -zkAddress=localhost:2123/kafka -port 9876
```
### 3) Incluir Schemas e Tabelas no Apache Pinot
Utilizar a [API do Pinot](http://localhost:9000/help) para incluir [Schemas do Pinot](https://github.com/fxmuld3r/puc_airlines_reviews_sentiment_analysis/blob/main/puc_airlines_reviews_sentiment_analysis/settings/schemas_pinot.txt) de dados referentes às mensagens que serão armazenadas nos tópicos Kafka 
Incluir [Realtime Tables](http://localhost:9000/#/tables) via interface web do Pinot apontadas para o broker "localhost:9876", com os seguintes nomes:
- AirlinesReviewsKafkaTopic para o tópico "airlines-reviews-kafka-topic";
- AirlinesReviewsTransformatedKafkaTopic para o tópico "airlines-reviews-transformed-kafka-topic";
- AirlinesReviewsSentimentAnalisysKafkaTopic para o tópico "airlines-reviews-sentiment-analysis-kafka-topic'";
### 4) Executar API de Mock de Dados de Testes  (porta 5000)
Quando acionada a API realiza a leitura de dados do arquivo de massa de dados (CSV) e aciona a API de Ingestão de Dados:
```sh
~/puc_airlines_reviews_sentiment_analysis/mock$ python3 airlines_reviews_api_data_mock.py
```
### 5) Executar API de Ingestão de Avaliações de Viagens  (porta 5001)
Quando acionada, a API recepciona Avaliações de Viagens e armazena (JSON) as mensagens no tópico Kafka "airlines-reviews-kafka-topic":
```sh
~/puc_airlines_reviews_sentiment_analysis/api$ python3 airlines_reviews_api_data_ingestion.py
```
### 6) Executar Scheduler para Mock de Dados de Testes
O sheduler aciona a API de mock de dados para acionar a API de Ingestão:
```sh
~/puc_airlines_reviews_sentiment_analysis/mock$ python3 airlines_reviews_mock_scheduler.py
```
### 7) Consultar Dados Ingeridos de Avaliações de Viagens no Apache Pinot
http://localhost:9000/#/query?query=select+*+from+AirlinesReviewsKafkaTopic+limit+10&tracing=false&useMSE=false
