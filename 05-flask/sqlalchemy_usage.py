from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/temp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Role(db.Model):
		__tablename__ = 'roles'
		id = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String(64), unique=True)
		user = db.relationship('User', backref='role')


class User(db.Model):
		__tablename__ = 'users'
		id = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String(64), unique=True)
		email = db.Column(db.String(64), unique=True)
		pswd = db.Column(db.String(64))
		role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


if __name__ == '__main__':
		db.session.add_all([Role(name='test')])
		db.session.commit()
