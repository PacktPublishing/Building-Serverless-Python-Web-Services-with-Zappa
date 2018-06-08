from models import QuoteModel
from mashape import fetch_quote
from sns import QuoteSubscription
from async import async_publish


def set_quote_of_the_day(event, context):
    QuoteModel.create(**fetch_quote())


def publish_quote_of_the_day(event, context):
    quote = fetch_quote()
    async_publish(message=quote['quote'])