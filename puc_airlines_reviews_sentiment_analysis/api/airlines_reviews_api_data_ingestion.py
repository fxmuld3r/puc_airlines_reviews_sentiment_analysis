#!/usr/bin/env python
# encoding: utf-8

import locale
import traceback
import pandas as pd
from flask import Flask, request, jsonify, Response, json
from kafka import KafkaProducer

# import module from parental folder
import sys

sys.path.append('../')
from settings.settings import BROKER, AIRLINE_REVIEW_MESSAGES_TOPIC

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # define location as Brasil
pd.set_option('display.width', 600)  # expand screen layout
pd.set_option('display.max_columns', 15)  # expand screen layout

app = Flask(__name__)


class AirlineReviewApiProducer:
    """airlines reviews ingestion api - consume airlines reviews and producer to kafka airlines reviews topic"""

    def __init__(self):
        pass

    @staticmethod
    @app.route('/reviews', methods=['POST'])
    def insert_record():
        """insert (producer) message in kafka topic"""
        try:

            message = request.get_json(force=True)
            print('data from client:', message)

            # broker = 'localhost:9092'
            # broker = 'localhost:9876'
            broker = BROKER
            # topic = 'airlines-reviews-topic'
            topic = AIRLINE_REVIEW_MESSAGES_TOPIC
            producer = KafkaProducer(bootstrap_servers=broker,
                                     value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                     acks='all',
                                     retries=3)

            # write message
            future = producer.send(topic, message)
            producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")

            return Response(json.dumps(message), mimetype='application/json'), 200

        except (Exception,):
            traceback.print_exc()
            return jsonify({'error': 'data not found'})


if __name__ == '__main__':
    airlineReviewApiProducer = AirlineReviewApiProducer
    # app.run(debug=True, host="0.0.0.0")
    app.run(debug=True, port=5001)
    # airlineReviewApiProducer.app.run(debug=True)
