from flask_restful import Api
from flask import Flask

from sep_auth import Sep10Auth
import settings


app = Flask(__name__)
api = Api(app)


if settings.SEP10AUTH == True:
    api.add_resource(Sep10Auth, '/api/sep-auth', endpoint='sep_auth')


if __name__ == '__main__':
    app.run(debug=True)