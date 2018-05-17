from models import QuoteModel
from mashape import fetch_quote


def set_quote_of_the_day(event, context):
    QuoteModel.create(**fetch_quote())
