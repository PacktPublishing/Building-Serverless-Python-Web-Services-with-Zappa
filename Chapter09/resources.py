import os
import re
import datetime
import requests
import falcon
import boto3

from models import QuoteModel, OTPModel
from mashape import fetch_quote
from async import async_subscribe, async_unsubscribe, async_send_otp


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
            otp = req.get_param('otp')
            otp_data = OTPModel.select().where(OTPModel.mobile_number == mobile_number, OTPModel.otp == otp, OTPModel.is_verified == False)
            if mobile_number and otp_data.exists():
                otp_data = otp_data.get()
                otp_data.is_verified = True
                otp_data.save()
                async_subscribe(mobile_number)
                resp.media = {"message": "Congratulations!!! You have successfully subscribed for daily famous quote."}
            elif mobile_number and not otp_data.exists():
                async_send_otp(mobile_number)
                resp.media = {"message": "An OTP verification has been sent on mobile {0}. To complete the subscription, Use OTP with this URL pattern https://quote-api.abdulwahid.info/subscribe?mobile={0}&otp=xxxx.".format(mobile_number)}
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