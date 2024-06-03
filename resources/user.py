from flask_restful import Resource, reqparse
from models import User
from db import db
from studio_ghibli_api import fetch_data_by_role

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help="Username cannot be blank!")
parser.add_argument('role', type=str, required=True, help="Role cannot be blank!")

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = db.session.get(User, user_id)
            if user:
                return {'id': user.id, 'username': user.username, 'role': user.role}, 200
            return {'message': 'User not found'}, 404
        users = User.query.all()
        return [{'id': user.id, 'username': user.username, 'role': user.role} for user in users], 200

    def post(self):
        data = parser.parse_args()
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400
        new_user = User(username=data['username'], role=data['role'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

    def put(self, user_id):
        data = parser.parse_args()
        user = db.session.get(User, user_id)
        if user:
            user.username = data['username']
            user.role = data['role']
            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        return {'message': 'User not found'}, 404

    def delete(self, user_id=None):
        if user_id:
            user = db.session.get(User, user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return {'message': 'User deleted successfully'}, 200
            return {'message': 'User not found'}, 404
        count = User.query.delete()
        db.session.commit()
        return {'message': f'{count} users deleted successfully'}, 200

class UserGhibliResource(Resource):
    def get(self, user_id):
        user = db.session.get(User, user_id)
        if user:
            data, status_code = fetch_data_by_role(user.role)
            return data, status_code
        return {'message': 'User not found'}, 404
