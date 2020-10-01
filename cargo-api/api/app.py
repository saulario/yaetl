
import logging

from flask import Flask, request
from flask_restful import Api

import cargo.default as default

import resources.inf.usu as usu

logging.basicConfig(level=logging.DEBUG, format=default.LOG_FORMAT)
log = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

api.add_resource(usu.List, "/inf/usu")
api.add_resource(usu.Edit, "/inf/usu/<int:ususeq>")

if __name__ == "__main__":
    app.run(debug=True)