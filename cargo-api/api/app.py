
import logging

from flask import Flask, request
from flask_restful import Api, fields

import cargo.default as default

import resources.inf.usu as usu

logging.basicConfig(level=logging.DEBUG, format=default.LOG_FORMAT)
log = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

fields.Integer

api.add_resource(usu.Dispatcher, "/inf/usu",
        "/inf/usu/<int:ususeq>")

