from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_user import roles_required

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    company = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(32))
    phone = db.Column(db.String(12))
    role = db.Column(db.Boolean)

    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Contract(db.Model):
    contract_id = db.Column(db.String(140), primary_key=True)
    producer = db.Column(db.String(100), index=True)
    marketer = db.Column(db.String(100), index=True)
    contract_type = db.Column(db.String)
    day_due = db.Column(db.Integer)
    active = db.Column(db.Boolean)

    def __repr__(self):
        return '<Contract ID: {}>'.format(self.contract_id)

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles data model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class Nom(db.Model):
    nom_id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.String(140), db.ForeignKey('contract.contract_id'))
    day_nom = db.Column(db.DateTime, index=True)
    day_nom_value = db.Column(db.Integer)
    downstream_contract = db.Column(db.Integer)
    downstream_ba = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    edit = db.Column(db.Boolean)
    published_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Nom ID: {}>'.format(self.id)
