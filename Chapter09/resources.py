import os
import re
import datetime
import requests
import falcon
import boto3

from models import QuoteModel
from mashape import fetch_quote
from async import async_subscribe, async_unsubscribe


class DailyQuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            data = QuoteModel.select().where(QuoteModel.created_at == datetime.date.today())
            if data.exists():
                data = data.get()
                resp.media = {'quote': data.quote, 'author': data.author, 'category': data.category}
            else:
                quote = fetch_quote()
                QuoteModel.create(**quote)
                resp.media = quote
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, str(e))


class SubscribeQuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            mobile_number = '+{}'.format(req.get_param('mobile'))
            if mobile_number:
                async_subscribe(mobile_number)
                resp.media = {"message": "Congratulations!!! You have successfully subscribed for daily famous quote."}
            else:
                raise falcon.HTTPError(falcon.HTTP_500, 'Require a valid mobile number as a query parameter. e.g https://<API_ENDPOINT>/subscribe?mobile=XXXXXXX')
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, str(e))


class UnSubscribeQuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            mobile_number = '+{}'.format(req.get_param('mobile'))
            if mobile_number:
                async_unsubscribe(mobile_number)
                resp.media = {"message": "You have successfully unsubscribed from daily famous quote. See you again."}
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, str(e))


api = falcon.API()
api.add_route('/daily', DailyQuoteResource())
api.add_route('/subscribe', SubscribeQuoteResource())
api.add_route('/unsubscribe', UnSubscribeQuoteResource())