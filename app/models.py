from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único do usuário
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email do usuário
    password = db.Column(db.String(60), nullable=False)  # Senha do usuário

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
