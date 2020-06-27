from flask import Flask
from api.controllers import upepo
from api.model import db_access
from home.controllers import home

app = Flask(__name__)
app.register_blueprint(home, url_prefix='/')
app.register_blueprint(upepo, url_prefix='/upepo/v1/')
#db_access()