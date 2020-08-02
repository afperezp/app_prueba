from flask import request
from flask_restplus import Resource

from ..util.dto import PostDto


api = PostDto.api
_post = PostDto.post