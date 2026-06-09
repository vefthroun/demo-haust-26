from flask import Flask, render_template, request
app = Flask(__name__)

from app import index
from app import login
from app import signup
from app import profile
from app import form
from app import errors
#from app import userlist