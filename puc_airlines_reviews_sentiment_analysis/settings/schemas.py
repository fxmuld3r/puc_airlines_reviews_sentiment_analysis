# tweets json [schema] definition
from pyspark.sql.types import StructType, StructField, StringType

airline_review_schema_json = StructType([
    StructField('col_index', StringType(), True),
    StructField('departure_city', StringType(), True),
    StructField('flight_date', StringType(), True),
    StructField('airline', StringType(), True),
    StructField('customer_review_original_language', StringType(), True),
    StructField('language', StringType(), True)
])

airline_review_schema_translated_json = StructType([
    StructField('col_index', StringType(), True),
    StructField('departure_city', StringType(), True),
    StructField('flight_date', StringType(), True),
    StructField('airline', StringType(), True),
    StructField('customer_review_original_language', StringType(), True),
    StructField('language', StringType(), True),
    StructField('text_translated', StringType(), True)
])

airline_review_schema_sentiment_json = StructType([
    StructField('col_index', StringType(), True),
    StructField('departure_city', StringType(), True),
    StructField('flight_date', StringType(), True),
    StructField('airline', StringType(), True),
    StructField('customer_review_original_language', StringType(), True),
    StructField('language', StringType(), True),
    StructField('text_translated', StringType(), True),
    StructField('polarity', StringType(), True),
    StructField('subjectivity', StringType(), True),
    StructField('sentiment_result', StringType(), True)
])
