# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.post_controller import api as post_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='API TASTEA',
          version='1.0',
          description='A simple API for TASTEA'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(post_ns, path='/post')