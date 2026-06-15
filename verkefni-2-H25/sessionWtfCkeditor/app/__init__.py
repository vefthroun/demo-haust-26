from flask import Flask

app = Flask(__name__)

from app import index
from app import signup
from app import signin
from app import profile
from app import errors