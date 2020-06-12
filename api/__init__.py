from flask import Flask
from flasgger import Swagger
import os.path
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config.from_object('config')
if os.path.isfile(os.path.join(BASE_DIR, 'config_prod.py')):
    import config_prod
    app.config.update(**config_prod.__dict__)

Swagger(app, template=app.config['SWAGGER_TEMPLATE'])

handler = app.config['LOGGING_HANDLER']
handler.setFormatter(app.config['LOGGING_FORMATTER'])
if len(app.logger.handlers) > 0:
    app.logger.handlers[0] = handler
else:
    app.logger.addHandler(handler)

app.logger.setLevel(app.config['LOGGING_LEVEL'])
app.url_map.converters['regex'] = RegexConverter

from api import views, api_response


