# import libraries
from pyspark.sql import SparkSession
from textblob.exceptions import TextBlobError, TranslatorError, NotTranslated
from pyspark.sql.functions import col, from_json, lower, udf
import pyspark.sql.functions as f
from textblob import TextBlob

# import module from parental folder
import sys
sys.path.append('../')
from settings.settings import *
from settings.schemas import *


class AirlineReviewStreamingTransformation:
    """airlines reviews - producer customer_review_original_language transformed in kafka topic"""

    @staticmethod
    def to_lower_str_columns(df):
        """convert customer_review_original_language to lowercase"""
        return df.withColumn("customer_review_original_language", lower(df.customer_review_original_language))

    @staticmethod
    def remove_spaces(df):
        """remove spaces from customer_review_original_language"""
        return df.withColumn("customer_review_original_language", f.regexp_replace(
            col("customer_review_original_language"), "\s+", " "))

    @staticmethod
    def remove_line_breaks(df):
        """remove line breaks from customer_review_original_language"""
        return df.withColumn("customer_review_original_language", f.regexp_replace(
            col("customer_review_original_language"), r'\[\[(?:[^|\]]*\|)?([^\]]*)]]', ""))

    @staticmethod
    def decode_text(df):
        """decode customer_review_original_language to UTF-8"""
        return df.withColumn("customer_review_original_language", f.decode(
            "customer_review_original_language", "UTF-8"))

    @staticmethod
    def remove_uls(df):
        """remove urls from customer_review_original_language"""
        return df.withColumn(
            "customer_review_original_language", f.regexp_replace(f.regexp_replace(
                "customer_review_original_language",
                r'https?:\/\/\S*', ""), '""', ''))

    @classmethod
    def translate_sentence_to_english(cls, customer_review_original_language, language):
        """translate unit customer_review_original_language sentences to english"""

        try:
            print(3 * "")
            print("1>>>>>>>>>>>>>> original_language", language)
            print("2>>>>>>>>>>>>>> original_text ", customer_review_original_language)

            # define language translation
            if language == 'portuguese' or language == 'spanish' or language == 'italian' or language == 'french' or \
                    language == 'arabic' or language == 'german' or language == 'chinese' or language == 'turc' \
                    or language == 'indian' or language == 'dutch' or language == 'japanese' or language == 'greek':

                # identify acronym language
                if language == 'portuguese':
                    language_acronym = 'pt'
                elif language == 'spanish':
                    language_acronym = 'es'
                elif language == 'italian':
                    language_acronym = 'it'
                elif language == 'french':
                    language_acronym = 'fr'
                elif language == 'arabic':
                    language_acronym = 'ar'
                elif language == 'german':
                    language_acronym = 'de'
                elif language == 'chinese':
                    language_acronym = 'zh-tw'
                elif language == 'turc':
                    language_acronym = 'tr'
                elif language == 'indian':
                    language_acronym = 'hi'
                elif language == 'dutch':
                    language_acronym = 'nl'
                elif language == 'japanese':
                    language_acronym = 'jp'
                elif language == 'greek':
                    language_acronym = 'el'
                else:
                    language_acronym = 'en'

                text_translated = str(TextBlob(
                    customer_review_original_language).translate(from_lang=language_acronym, to='english'))

            elif language == 'english':
                text_translated = str(customer_review_original_language)
            else:
                text_translated = "Not translated"

            print("3>>>>>>>>>>>>>> text_translated", text_translated)

        except NotTranslated:
            return "Not translated"
        except TranslatorError:
            return "Not translated"
        except TextBlobError:
            return "Not translated"
        else:
            return text_translated

    @classmethod
    def translate(cls, df):
        """translate customer_review_original_language sentences dataframe to english"""

        # register personal function (udf)
        translate_sentences_udf = udf(lambda sentence, language: cls.translate_sentence_to_english(sentence, language),
                                      StringType())

        # create translated column
        df = df.withColumn("text_translated",
                           translate_sentences_udf(f.col("customer_review_original_language"), f.col("language")))
        return df

    @classmethod
    def text_transformation(cls):
        """airline review client - transform and producer text and write to kafka topic"""

        try:

            # init spark session
            spark = SparkSession \
                .builder \
                .appName('customer-review-spark-streaming-transformation') \
                .config("spark.jars.packages", SPARK_VERSION) \
                .getOrCreate()

            # remove WARNs
            spark.conf.get("spark.sql.adaptive.enabled", "False")

            # set log level to info
            # spark.sparkContext.setLogLevel("INFO")

            # read topic dataframe
            df_topic_airline_review = spark \
                .readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", BROKER) \
                .option("subscribe", AIRLINE_REVIEW_MESSAGES_TOPIC) \
                .option("startingOffsets", "earliest") \
                .option("failOnDataLoss", "false") \
                .load() \
                .selectExpr("CAST(value AS STRING)") \
                .withColumn("jsonData", from_json(col("value"), airline_review_schema_translated_json)) \
                .select("jsonData.*")

            # print schema from dataframe
            df_topic_airline_review.printSchema()

            # select airlines reviews in specifics idioms
            # and transform airlines reviews
            df_topic_airline_review = df_topic_airline_review \
                .select("col_index", "departure_city", "flight_date", "airline", "customer_review_original_language",
                        "language") \
                .transform(cls.remove_spaces) \
                .transform(cls.remove_line_breaks) \
                .transform(cls.decode_text) \
                .transform(cls.to_lower_str_columns) \
                .transform(cls.remove_uls) \
                .transform(cls.translate)

            # .option("checkpointLocation", "/tmp/airline_checkpoint_transformation/checkpoint") \
            # .option("checkpointLocation", CHECKPOINT) \
            # .option("checkpointLocation", "/tmp/airlines_reviews_checkpoint_transformation3/checkpoint") \

            # write text tweet json in Kafka topic
            df_topic_airline_review \
                .selectExpr("CAST(to_json(struct(*)) AS STRING) AS value") \
                .writeStream \
                .format("kafka") \
                .outputMode("append") \
                .option("topic", AIRLINE_REVIEW_TRANSFORMED_MESSAGES_TOPIC) \
                .option("kafka.bootstrap.servers", BROKER) \
                .option("checkpointLocation", CHECKPOINT_TRANSFORMATION) \
                .start()

            # print data in console
            df_topic_airline_review \
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
    airlineReviewStreamingTransformation = AirlineReviewStreamingTransformation
    airlineReviewStreamingTransformation.text_transformation()
