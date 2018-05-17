import os
import requests

from models import QuoteModel

def fetch_quote():
    response = requests.get(
        os.environ.get('Mashape_API_Endpoint'),
        headers={
            'X-Mashape-Key': os.environ.get('X_Mashape_Key'),
            'Accept': 'application/json'
        }
    )
    if response.status_code == 200:
        return response.json()[0]
    return response.json()


def set_quote_of_the_day(event, context):
    QuoteModel.create(**fetch_quote())
