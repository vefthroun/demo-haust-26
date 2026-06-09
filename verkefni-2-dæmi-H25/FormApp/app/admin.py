from app import app
from flask import Flask, render_template, request

@app.route("/admin", methods = ['POST', 'GET'])
def admin():
    title="Ritstjórn"
    # birtum formið
    if request.method == 'GET':
        return render_template("admin.html", title=title)
    
    # formvinnsla 
    if request.method == 'POST':
        # sækjum gildin úr name breytum úr formi  
        kwargs = {
            "title": request.form["title"],
            "isbn": request.form["isbn"],
            "author": request.form["author"],
            "about": request.form["about"],
            "timestamp": request.form["timestamp"]
        }    
        print(kwargs)
        return render_template("index.html", **kwargs)
    
# *args og **kwargs útskýrt: https://realpython.com/python-kwargs-and-args/
# Working with Forms in Flask (myndband): https://www.youtube.com/watch?v=KW_ItlO5kR4
