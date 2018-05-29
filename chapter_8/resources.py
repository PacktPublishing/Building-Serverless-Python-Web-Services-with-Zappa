import os
import datetime
import requests
import falcon

from models import QuoteModel
from mashape import fetch_quote

class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        if req.get_param('type') in ['daily', None]:
            data = QuoteModel.select().where(QuoteModel.created_at == datetime.date.today())
            if data.exists():
                data = data.get()
                resp.media = {'quote': data.quote, 'author': data.author, 'category': data.category}
            else:
                quote = fetch_quote()
                QuoteModel.create(**quote)
                resp.media = quote
        elif req.get_param('type') == 'random':
            resp.media = fetch_quote()
        else:
            raise falcon.HTTPError(falcon.HTTP_400,'Invalid Quote type','Supported types are \'daily\' or \'random\'.')

api = falcon.API()
api.add_route('/quote', QuoteResource())