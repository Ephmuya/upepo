from flask import Flask
from api.controllers import upepo
app = Flask(__name__)
app.register_blueprint(upepo, url_prefix='/upepo/v1/')