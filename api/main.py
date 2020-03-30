from flask import Flask
from flask_restful import Api

from sep10 import sep10_mod
from info import info_mod
from deposit import deposit_mod
from withdraw import withdraw_mod

import settings


app = Flask(__name__)
app.register_blueprint(sep10_mod)
app.register_blueprint(info_mod)
app.register_blueprint(deposit_mod)
app.register_blueprint(withdraw_mod)

if settings.SEP10AUTH == True:
    app.register_blueprint(sep10_mod)

if __name__ == '__main__':
    app.run(debug=True)
