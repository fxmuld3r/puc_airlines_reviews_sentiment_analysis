# spark parameters settings
# BROKER = 'localhost:9092'
BROKER = 'localhost:9876'
SPARK_VERSION = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2"

# kafka parameters settings
AIRLINE_REVIEW_MESSAGES_TOPIC = 'airlines-reviews-kafka-topic'
AIRLINE_REVIEW_TRANSFORMED_MESSAGES_TOPIC = 'airlines-reviews-transformed-kafka-topic'
AIRLINE_REVIEW_SENTIMENT_ANALYSIS_MESSAGES_TOPIC = 'airlines-reviews-sentiment-analysis-kafka-topic'
STATING_OFFSET = 'latest'
CHECKPOINT_TRANSFORMATION = '/tmp/spark_checkpoint/airlines_reviews_checkpoint_transformation3'
CHECKPOINT_AI = '/tmp/spark_checkpoint/airlines_reviews_checkpoint_ai3'
# CHECKPOINT = '/tmp/airlines_reviews_checkpoint_transformation/checkpoint'

print("========================================================================")
print("BOOTSTRAP_SERVER ", BROKER)
print("AIRLINE_REVIEW_MESSAGES_TOPIC ", AIRLINE_REVIEW_MESSAGES_TOPIC)
print("AIRLINE_REVIEW_TRANSFORMED_MESSAGES_TOPIC ", AIRLINE_REVIEW_TRANSFORMED_MESSAGES_TOPIC)
print("AIRLINE_REVIEW_SENTIMENT_ANALYSIS_MESSAGES_TOPIC ", AIRLINE_REVIEW_SENTIMENT_ANALYSIS_MESSAGES_TOPIC)
print("STATING_OFFSET ", STATING_OFFSET)
print("CHECKPOINT_TRANSFORMATION ", CHECKPOINT_TRANSFORMATION)
print("CHECKPOINT_AI ", CHECKPOINT_AI)
# print("CHECKPOINT ", CHECKPOINT)
print("========================================================================")
