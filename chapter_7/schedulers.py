import os
import requests

from models import QuoteModel


def fetch_quote(event, context):
    response = requests.get(os.environ.get('Mashape_API_Endpoint'),
        headers={
            "X-Mashape-Key": os.environ.get('X_Mashape_Key'),
            "Accept": "application/json"
        }
    )
    if response.status_code == 200:
        QuoteModel.create(**response.json()[0])

if __name__ == '__main__':
    fetch_quote({},{})