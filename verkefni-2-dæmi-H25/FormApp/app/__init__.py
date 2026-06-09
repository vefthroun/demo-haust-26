from flask import Flask

app = Flask(__name__)

from app import index
from app import login
from app import signup
from app import admin
from app import errors