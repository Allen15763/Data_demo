from . import db, login_manager
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedSerializer as Serializer
from datetime import datetime

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        # return '<User %r>' % self.username
        return "<User(username='%s', role_id='%s')>" % (self.username, self.role_id)

class Test_data(db.Model):
    __tablename__ = 'test_data'
    id = db.Column(db.Integer, primary_key=True)
    Sepal_Length = db.Column(db.FLOAT, nullable=False)
    Sepal_Width = db.Column(db.FLOAT, nullable=False)
    Petal_Length = db.Column(db.FLOAT, nullable=False)
    Species = db.Column(db.String(64), nullable=False)
    Petal_Width = db.Column(db.FLOAT, nullable=False)
    SpeciesId = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        content = ' : '.join([
            'id=' + str(self.id),
            'Sepal_Length=' + str(self.Sepal_Length),
            'Sepal_Width=' + str(self.Sepal_Width)
        ])
        return '<Test_data(' + content + ')>'



"""
Exception: Missing user_loader or request_loader. Refer to http://flask-login.readthedocs.io/#how-it-works for more info.
務必使用，不然會在初始化時就出錯

保護路由p108
"""
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


