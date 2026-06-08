from app import app
from flask import Flask, render_template, request, redirect, url_for

# ATHUGIÐ > 'app = Flask(__name__)' má ekki vera í gangi hér, routið er í __init__.py

@app.route("/", methods=["GET", "POST"])
def index():
    # index tekur við gögnum  (**kwargs) úr /userprofile [post]
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
    return render_template("index.html")


# App run er í rótinni = app.py 
'''if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)'''