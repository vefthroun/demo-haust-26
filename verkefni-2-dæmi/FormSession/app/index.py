from app import app
from flask import render_template, request, session, flash, redirect

# login
@app.route("/", methods=['GET','POST'])
def index():
    title="Bókahillan"
    
    if 'blogg' not in session:
        #býr til blogg
        session['blogg'] = []
    else:
        session['blogg'].reverse() 
    
    return render_template("index.html", title=title)