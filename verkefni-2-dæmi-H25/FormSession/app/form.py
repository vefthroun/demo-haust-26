from app import app
from flask import render_template, request, session, redirect, url_for, flash

@app.route("/form", methods = ['POST', 'GET'])
def form():
    # birtum formið
    if request.method == 'GET':
        return render_template("form.html")
    
    # formvinnsla 
    if request.method == 'POST':
        # sækjum gildin úr name breytum úr formi  
        kwargs = {
            "title": request.form["title"],
            "isbn": request.form["isbn"],
            "author": request.form["author"],
            "timestamp": request.form["timestamp"]
        }    
        return render_template("form_result.html", **kwargs)
        # *args og **kwargs útskýrt: https://realpython.com/python-kwargs-and-args/
