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
- Apache Airflow 2.1.0;
- Apache Kafka;
- Apache Parquet;
- Apache Pinot 0.12.0;
- Apache Spark 3.4.1;
- Apache Spark Streaming 3.4.1;
- Apache Superset;
- Apache ZooKeeper (embutido no Apache Pinot);
- Docker 20.10.24;
- Flask 2.3.2;
- MongoDB;
- Python 3.10.9;
- TextBlob 0.17.1;

## Instalação
Para executar o projeto, é necessário instalar as ferramentas listadas na seção acima, conforme versões detalhadas.

## Arquivo de Dados com Massa de Testes
[Massa de Dados](https://github.com/fxmuld3r/puc_airlines_reviews_sentiment_analysis/tree/main/puc_airlines_reviews_sentiment_analysis/mock/data)

## Paso a Passo de Execução do Projeto

### Apache Pinot com Zookeper
Iniciar o Apache Pinot (o zookeper é carregado automaticamente):
```sh
~/apache-pinot-0.12.0-bin$ bin/quick-start-streaming.sh
```
A interface do Pinot pode ser acessa através do link:  http://localhost:9000

### Apache Kafka no Pinot
Iniciar o Apache Kafka (com porta personalizada 9876) embutido no Apache Pinot
```sh
~/apache-pinot-0.12.0-bin$ sudo bin/pinot-admin.sh  StartKafka -zkAddress=localhost:2123/kafka -port 9876
```

