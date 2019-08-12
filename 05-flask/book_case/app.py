from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql

pymysql.install_as_MySQLdb()
app = Flask(__name__)


class AppConfig(object):
    """app配置文件"""
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/temp'
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 设置app跟踪数据库
    SECRET_KEY = 'naruto,hyf'


app.config.from_object(AppConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # 增加migrate扩展


class Author(db.Model):
    """作者模型类"""
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    books = db.relationship('Book', backref='author')


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))


class PostForm(FlaskForm):
    """提交表单模型类"""
    author_name = StringField(label='作者', validators=[DataRequired('作者姓名必填')])
    book_name = StringField(label='书名', validators=[DataRequired('书名必填')])
    submit = SubmitField(label='保存')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        # 表单验证通过，提取数据
        author_name = form.author_name.data
        book_name = form.book_name.data
        author = Author.query.filter_by(name=author_name).first()
        if author is None:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
        book = Book(name=book_name, author=author)
        db.session.add(book)
        db.session.commit()
    authors = Author.query.all()
    return render_template('index.html', authors=authors, form=form)


