#!/usr/bin/env python
# encoding: utf-8
import locale
import traceback
import pandas as pd
from flask import Flask, request, jsonify, Response, json

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # define location as Brasil
pd.set_option('display.width', 600)  # expand screen layout
pd.set_option('display.max_columns', 15)  # expand screen layout

app = Flask(__name__)


class AirlineReviewApiDataMock:
    """airlines reviews api - get mock data airlines simulated reviews"""

    def __init__(self):
        pass

    @staticmethod
    @app.route('/reviews/<criteria>', methods=['GET'])
    def get_records(criteria):
        """get records form csv file to simulate call of airlines api """

        try:

            # get argument to select records
            first_row_selected = int(request.args.get('first_row_selected'))
            last_row_selected = int(request.args.get('last_row_selected'))

            # loads mock data records
            df_customer_review = pd.read_csv('data/customer_review_result_2.csv',
                                             sep='|', encoding='utf-8')

            # filter columns to use
            df_filtered_customer_review = (df_customer_review[[
                'col_index', 'departure_city', 'flight_date', 'airline', 'language',
                'customer_review_original_language']].loc[first_row_selected:last_row_selected])

            # convert to dict
            dict_customer_review = df_filtered_customer_review.to_dict('records')

            # convert records to json
            json_customer_review = {
                "col_index": str(dict_customer_review[0].get("col_index")),
                "departure_city": str(dict_customer_review[0].get("departure_city")),
                "flight_date": str(dict_customer_review[0].get("flight_date")),
                "airline": str(dict_customer_review[0].get("airline")),
                "language": str(dict_customer_review[0].get("language")),
                "customer_review_original_language": str(
                    dict_customer_review[0].get("customer_review_original_language"))
            }

            # define json to response
            json_customer_review = json.dumps(json_customer_review, indent=4)
            print(">>>>> airline review data mock: ", json_customer_review)

            return Response(json_customer_review, mimetype='application/json'), 200

        except (Exception,):
            traceback.print_exc()
            return jsonify({'error': 'data not found'})


if __name__ == '__main__':
    airlineReviewApiDataMock = AirlineReviewApiDataMock
    # app.run(debug=True, host="0.0.0.0")
    app.run(debug=True)
    # airlineReviewApi.app.run(debug=True)
