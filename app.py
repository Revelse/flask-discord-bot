from threading import Thread

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

import bot
import settings

# Make a thread for our bot to run on.
t = Thread(target=bot.run)
t.start()

# Create our app
app = Flask(__name__)
app.secret_key = settings.APP_SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Let's create a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(settings.DATABASE_FILE)
db = SQLAlchemy(app)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user_num = db.Column(db.Integer, unique=True, autoincrement=True)
    permissions = db.Column(db.Integer)

    def __init__(self, name, user_num, permissions=0):
        self.name = name
        self.user_num = user_num
        self.permissions = permissions

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<User: {self.name}>'


class BotCommand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    command_send = db.Column(db.String(100))

    def __str__(self):
        return self.name


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(100), unique=True)

    def __str__(self):
        return self.answer


# App routes
@app.route('/')
def index():
    return '<a href="/admin/">Admin</a>'


# Build database
db.create_all()

# Admin model
admin = Admin(app, name='flask-discord-bot', template_mode='bootstrap3')

# Admin views
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Answers, db.session))
admin.add_view(ModelView(BotCommand, db.session))
