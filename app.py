from flask import Flask
from flask_restful import Api
from config import Config, DevelopmentConfig, ProductionConfig
from db import db
from resources.user import UserResource, UserGhibliResource

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
api = Api(app)

db.init_app(app)

with app.app_context():
    db.create_all()

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(UserGhibliResource, '/users/<int:user_id>/ghibli')

if __name__ == '__main__':
    app.run(debug=True)
