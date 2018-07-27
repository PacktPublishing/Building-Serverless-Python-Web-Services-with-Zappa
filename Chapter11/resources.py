import falcon
from zappa.async import task
from mashape import fetch_quote


class RandomQuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            resp.media = fetch_quote()
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, str(e))


@task
def async_task():
    raise ValueError("Async Failure Exception")


class AsyncTaskResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            async_task()
            resp.media = 'Called async task'
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, str(e))

api = falcon.API()
api.add_route('/', RandomQuoteResource())
api.add_route('/async-failure', AsyncTaskResource())