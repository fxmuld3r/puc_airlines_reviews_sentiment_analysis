# import libraries
from pyspark.sql import SparkSession
from textblob import TextBlob
from pyspark.sql.functions import col, udf, from_json
import pyspark.sql.functions as f

# import module from parental folder
import sys

sys.path.append('../')
from settings.settings import *
from settings.schemas import *


class AirlineReviewStreamingSentimentAnalysis:
    """airlines reviews - producer sentiment analysis in kafka topic"""

    @classmethod
    def get_polarity(cls, translated_text):
        """detect sentiment analysis polarity"""
        return TextBlob(translated_text).sentiment.polarity

    @classmethod
    def get_subjectivity(cls, translated_text):
        """detect sentiment analysis subjectivity"""
        return TextBlob(translated_text).sentiment.subjectivity

    @classmethod
    def get_sentiment_analysis_result(cls, polarity_score):
        """get sentiment analysis result"""

        # print("-----polarity_score", polarity_score)
        if polarity_score < 0:
            return "Negative"
        elif polarity_score == 0:
            return "Neutral"
        else:
            return "Positive"

    @classmethod
    def process_sentiment_analysis(cls):
        """process sentiment analysis from airlines posts"""

        try:
            # init spark session
            spark_sentiment = SparkSession \
                .builder \
                .appName('airline-review-spark-streaming-sentiment-analysis') \
                .config("spark.jars.packages", SPARK_VERSION) \
                .config("spark.sql.repl.eagerEval.enabled", True) \
                .config("spark.sql.adaptive.enabled", False) \
                .getOrCreate()

            # read topic dataframe
            df_topic_airlines_sentiment = spark_sentiment \
                .readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", BROKER) \
                .option("subscribe", AIRLINE_REVIEW_TRANSFORMED_MESSAGES_TOPIC) \
                .option("startingOffsets", "earliest") \
                .option("failOnDataLoss", "false") \
                .load() \
                .selectExpr("CAST(value AS STRING)") \
                .withColumn("jsonData", from_json(col("value"), airline_review_schema_sentiment_json)) \
                .select("jsonData.*")

            # print schema from dataframe
            df_topic_airlines_sentiment.printSchema()

            # register personal function (udf)
            get_polarity_udf = udf(cls.get_polarity, StringType())
            get_subjectivity_udf = udf(cls.get_subjectivity, StringType())
            get_sentiment_analysis_result_udf = udf(cls.get_sentiment_analysis_result, StringType())

            # select transformed reviews from portuguese
            # translate reviews to english
            # calc polarity
            df_topic_airlines_sentiment = df_topic_airlines_sentiment \
                .select("col_index", "departure_city", "flight_date", "airline", "customer_review_original_language",
                        "language", "text_translated") \
                .withColumn("polarity", get_polarity_udf(f.col('text_translated'))) \
                .withColumn("subjectivity", get_subjectivity_udf(f.col('text_translated'))) \
                .withColumn("sentiment_result", get_sentiment_analysis_result_udf(f.col('polarity')))

            # .option("checkpointLocation", "/tmp/puc_checkpoint_transformation/checkpoint") \
            # .option("checkpointLocation", CHECKPOINT_TRANSFORMATION) \
            # .option("checkpointLocation", "/tmp/airlines_reviews_checkpoint_sentiment2/checkpoint") \

            # write text reviews json to Kafka topic
            df_topic_airlines_sentiment \
                .selectExpr("CAST(to_json(struct(*)) AS STRING) AS value") \
                .writeStream \
                .format("kafka") \
                .outputMode("append") \
                .option("topic", AIRLINE_REVIEW_SENTIMENT_ANALYSIS_MESSAGES_TOPIC) \
                .option("kafka.bootstrap.servers", BROKER) \
                .option("checkpointLocation", CHECKPOINT_AI) \
                .start()

            # .option("checkpointLocation", "/tmp/puc_checkpoint_transformation/checkpoint") \
            # .option("checkpointLocation", CHECKPOINT_TRANSFORMATION) \

            # # write appending data to parquet file
            # df_topic_airlines_sentiment \
            #     .select("*") \
            #     .writeStream \
            #     .format("parquet")  \
            #     .outputMode("append") \
            #     .option("path", "../data/airlines_reviews_parquet") \
            #     .option("checkpointLocation", CHECKPOINT) \
            #     .start()

            # print data in console
            df_topic_airlines_sentiment \
                .writeStream \
                .format('console') \
                .option("truncate", True) \
                .start() \
                .awaitTermination()

        except Exception as e:
            print("Error: " + str(e))
            print('Disconnected...')


# main spark program
if __name__ == '__main__':
    airlineReviewStreamingSentimentAnalysis = AirlineReviewStreamingSentimentAnalysis
    airlineReviewStreamingSentimentAnalysis.process_sentiment_analysis()
