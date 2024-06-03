from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, films, people, locations, species, vehicles

    def __repr__(self):
        return f"<User {self.username}>"
