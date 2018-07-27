import falcon
from falcon_multipart.middleware import MultipartMiddleware
from parser import doc_to_text


class DocParserResource:
    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            file_object = req.get_param('file')

            # file validation
            if file_object.type != 'application/msword' or file_object.filename.split('.')[-1] != 'doc':
                raise ValueError('Please provide a valid MS Office 93 -2003 document file.')

            # calling _doc_to_text method from parser.py
            text = doc_to_text(file_object)
            quote = {
                'text': text,
                'filename': file_object.filename
            }
            resp.media = quote
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, str(e))

api = falcon.API(middleware=[MultipartMiddleware()])
api.add_route('/doc-parser', DocParserResource())