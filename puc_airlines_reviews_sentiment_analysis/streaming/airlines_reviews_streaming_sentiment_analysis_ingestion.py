# import libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pymongo import MongoClient

# import module from parental folder
import sys

sys.path.append('../')
from settings.settings import *
from settings.schemas import *


class AirlineReviewStreamingSentimentAnalysisIngestion:
    """airlines reviews - ingestion sentiment analysis reviews"""

    @classmethod
    def write_machine_df_mongo(cls, target_df):

        # define mongodb uri address
        cluster = MongoClient("mongodb://andre:senha@localhost:27017/admin")

        # define database
        db = cluster["airlines_reviews"]

        # define collection
        collection = db.reviews

        # organize json data to stor in the database
        post = {
            "col_index": target_df.col_index,
            "departure_city": target_df.departure_city,
            "flight_date": target_df.flight_date,
            "airline": target_df.airline,
            "customer_review_original_language": target_df.customer_review_original_language,
            "language": target_df.language,
            "text_translated": target_df.text_translated,
            "polarity": target_df.polarity,
            "subjectivity": target_df.subjectivity,
            "sentiment_result": target_df.sentiment_result
        }

        # insert record in collecttion
        collection.insert_one(post)

    @classmethod
    def process_sentiment_analysis_ingestion(cls):
        """ingestion of sentiment analysis to no sql database"""

        try:
            # init spark session
            spark_sentiment = SparkSession \
                .builder \
                .appName('airline-review-spark-streaming-sentiment-analysis') \
                .config("spark.jars.packages", SPARK_VERSION) \
                .getOrCreate()

            # read topic dataframe
            df_topic_airlines_sentiment = spark_sentiment \
                .readStream \
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

            # mongodb ingestion
            df_topic_airlines_sentiment \
                .writeStream \
                .outputMode("append") \
                .foreach(cls.write_machine_df_mongo) \
                .start()

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
    airlineReviewStreamingSentimentAnalysisIngestion = AirlineReviewStreamingSentimentAnalysisIngestion
    airlineReviewStreamingSentimentAnalysisIngestion.process_sentiment_analysis_ingestion()
