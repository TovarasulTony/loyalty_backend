import os
import configparser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('config/models.ini')

app = Flask(__name__)
#app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
file_path = os.path.dirname(os.path.abspath(__file__))
head = os.path.split(file_path)[0]
#head = os.path.split(head)[0]
#print('sqlite:///' + head + "/site.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + head + "/site.db"
db = SQLAlchemy(app)
print("Tony")
print(__name__)

from flask_api import routes