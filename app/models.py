from datetime import datetime
from time import time
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from app import app
import jwt



class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(255), nullable=False, unique=True)
    company = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(32))
    phone = db.Column(db.String(12))
    role = db.Column(db.Integer, db.ForeignKey('permissions.role_id'), default='1')

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Contract(db.Model):
    contract_id = db.Column(db.Integer, primary_key=True, unique=True)
    producer = db.Column(db.String(100), db.ForeignKey('company.company_name'), index=True)
    marketer = db.Column(db.String(100), index=True)
    contract_type = db.Column(db.String)
    day_due = db.Column(db.Integer)
    active = db.Column(db.Boolean)

    def __repr__(self):
        return '<Contract ID: {}>'.format(self.contract_id)

class Nom(db.Model):
    nom_id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.contract_id'))
    day_nom = db.Column(db.DateTime, index=True)
    day_nom_value = db.Column(db.Integer)
    downstream_contract = db.Column(db.Integer)
    downstream_ba = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.delivery_id'))
    user = db.Column(db.String(64), db.ForeignKey('user.username'))
    edit = db.Column(db.Boolean)
    published_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean)

    def __repr__(self):
        return '<Nom ID: {}>'.format(self.nom_id)

class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50), unique=True, index=True)
    company_type = db.Column(db.String(8))
    status = db.Column(db.Boolean)

class Permissions(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(10))

class Delivery(db.Model):
    delivery_id = db.Column(db.Integer, primary_key=True)
    delivery_name = db.Column(db.String(50))