from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask import Flask

from helpers import validate_sep10_token
from sep_auth import Sep10Auth

import datetime
import settings
import os


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(settings.BASE_DIR, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if settings.SEP10AUTH == True:
    api.add_resource(Sep10Auth, '/api/sep-auth', endpoint='sep_auth')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)