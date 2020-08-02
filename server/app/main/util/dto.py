from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class PostDto:
    api = Namespace('post', description='post related to user')
    post = api.model('post', {
        'id': fields.Integer(required=True, description='post id'),
        'title': fields.String(required=True, description='post title'),
        'content': fields.String(required=True, description='post content'),
        'points': fields.Integer(required=True, description='post points')
    })
