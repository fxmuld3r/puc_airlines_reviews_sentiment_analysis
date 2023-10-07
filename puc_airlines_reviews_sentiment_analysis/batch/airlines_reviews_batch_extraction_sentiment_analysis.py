# import libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, from_json

# import module from parental folder
import sys

sys.path.append('../')
from settings.settings import *
from settings.schemas import *


class AirlineReviewBatchSentimentAnalysisExtraction:
    """airlines reviews - write sentiment analysis in parquet file"""

    @classmethod
    def process_write_to_parquet(cls):
        """process sentiment analysis from airlines posts"""

        try:
            # init spark session
            spark_sentiment = SparkSession \
                .builder \
                .appName('airline-review-spark-batch-parquet-sentiment-analysis') \
                .config("spark.jars.packages", SPARK_VERSION) \
                .config("spark.sql.repl.eagerEval.enabled", True) \
                .config("spark.sql.adaptive.enabled", False) \
                .getOrCreate()

            # read topic dataframe
            df_topic_airlines_sentiment = spark_sentiment \
                .read \
                .format("kafka") \
                .option("kafka.bootstrap.servers", BROKER) \
                .option("subscribe", AIRLINE_REVIEW_SENTIMENT_ANALYSIS_MESSAGES_TOPIC) \
                .option("startingOffsets", "earliest") \
                .option("failOnDataLoss", "false") \
                .load() \
                .selectExpr("CAST(value AS STRING)") \
                .withColumn("jsonData", from_json(col("value"), airline_review_schema_sentiment_json)) \
                .select("jsonData.*")

            # print schema from dataframe
            df_topic_airlines_sentiment.printSchema()

            # write appending data to parquet file
            df_topic_airlines_sentiment \
                .select("*") \
                .coalesce(1) \
                .write \
                .format("parquet") \
                .option('header', 'true') \
                .mode("overwrite") \
                .save("../data/airlines_reviews.parquet")

            # print data in console
            df_topic_airlines_sentiment \
                .write \
                .format('console') \
                .option("truncate", True)

        except Exception as e:
            print("Error: " + str(e))
            print('Disconnected...')


# main spark program
if __name__ == '__main__':
    airlineReviewBatchSentimentAnalysisExtraction = AirlineReviewBatchSentimentAnalysisExtraction
    airlineReviewBatchSentimentAnalysisExtraction.process_write_to_parquet()
