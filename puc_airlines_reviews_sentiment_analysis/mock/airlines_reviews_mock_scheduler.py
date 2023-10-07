import locale
import pandas as pd
import schedule
import time
import requests
from flask import json

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # define location as Brasil
pd.set_option('display.width', 600)  # expand screen layout
pd.set_option('display.max_columns', 20)  # expand screen layout


class AirlineReviewBatchSchedulerMock:
    """scheduler mock to request airlines reviews simulated api, and post to ingestion api reviews"""

    def __init__(self):
        """define local parameters"""

        self.url = "http://127.0.0.1:5000/"  # url to get airlines reviews
        self.params = {}  # parameters url
        self.headers = {}  # header url
        self.orders = []  # order url

        self.row_selected = 0  # first row dataset selected
        pass

    def get_airlines_reviews(self):
        """get airlines reviews from api simulator"""

        # url to get airlines reviews
        self.url = ("http://127.0.0.1:5000/reviews/rows?first_row_selected=" +
                    str(self.row_selected) +
                    "&last_row_selected=" + str(self.row_selected))

        # get airlines reviews from API simulator
        list_customer_review = requests.get(url=self.url).json()
        self.row_selected += 1

        return list_customer_review

    def set_airlines_reviews(self):
        """set airlines reviews to """

        # get simulated data from api
        json_airlines_reviews = self.get_airlines_reviews()

        # define post service data
        url = "http://127.0.0.1:5001/reviews"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        message = requests.post(url, data=json.dumps(json_airlines_reviews).encode('utf-8'), headers=headers)
        print("Response code return from mock API: ", message)

        return True


if __name__ == '__main__':
    airlineReviewBatchMockScheduler = AirlineReviewBatchSchedulerMock()
    time_seconds_request_records = 1  # define the time interval to request values from API Airlines Reviews Simulator
    schedule.every(time_seconds_request_records).seconds.do(airlineReviewBatchMockScheduler.set_airlines_reviews)

    while 1:
        schedule.run_pending()
        time.sleep(1)
