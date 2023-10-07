#!/usr/bin/env python
# encoding: utf-8

import locale
import traceback
from pinotdb import connect

import pandas as pd
from flask import Flask, request, jsonify, Response, json
from flask_cors import CORS

# import module from parental folder
import sys

sys.path.append('../')

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # define location as Brasil
pd.set_option('display.width', 600)  # expand screen layout
pd.set_option('display.max_columns', 15)  # expand screen layout

app = Flask(__name__)
CORS(app)  # To allow direct AJAX calls


class AirlineReviewNegativePostApi:
    """consume negatives sentiment analysis airlines reviews"""

    def __init__(self):
        pass

    @staticmethod
    @app.route('/negatives-reviews', methods=['GET'])
    def get_negatives_airlines_reviews():
        """consume negatives sentiment analysis airlines reviews from apache pinot"""
        try:

            # select send parameters
            selected_airline = request.args.get('selected_airline')
            flight_date = request.args.get('flight_date')

            print(selected_airline)
            print(flight_date)

            # connect to apache pinot e select data to api return
            conn = connect(host='localhost', port=8000, path='/query/sql', scheme='http')
            curs = conn.cursor()
            curs.execute("""
                SELECT * 
                  FROM AirlinesReviewsSentimentAnalisysKafkaTopic
                  WHERE airline like '""" + selected_airline + """' 
                  AND flight_date like '""" + flight_date + """%%' 
            """)

            # convert request result to dataframe
            df = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

            # convert to json
            message = df.to_json(orient='records')
            message = json.loads(message)

            print("message returned successfully...")

            return Response(json.dumps(message, indent=2, sort_keys=True), mimetype='application/json'), 200

        except (Exception,):
            traceback.print_exc()
            return jsonify({'error': 'data not found'})


if __name__ == '__main__':
    airlineReviewNegativePostApi = AirlineReviewNegativePostApi
    # app.run(debug=True, host="0.0.0.0")
    app.run(debug=True, port=5002)
    # airlineReviewNegativePostApi.app.run(debug=True)
