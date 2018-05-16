import os
import datetime
import requests
import falcon

from models import QuoteModel


class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        if req.get_param('type') in ['daily', None]:
            data = QuoteModel.select().where(QuoteModel.created_at == datetime.date.today()).get()
            resp.media = {'quote': data.quote, 'author': data.author, 'category': data.category}
        elif req.get_param('type') == 'random':
            response = requests.get(os.environ.get('Mashape_API_Endpoint'),
                headers={
                    'X-Mashape-Key': os.environ.get('X_Mashape_Key'),
                    'Accept': 'application/json'
                }
            )
            resp.media = response.json()[0]
        else:
            raise falcon.HTTPError(falcon.HTTP_400,'Invalid Quote type','Supported types are \'daily\' or \'random\'.')

api = falcon.API()
api.add_route('/quote', QuoteResource())