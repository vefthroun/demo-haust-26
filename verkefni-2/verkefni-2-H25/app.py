from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_ckeditor import CKEditor
app = Flask(__name__)

ckeditor = CKEditor(app)  # Frumstillum / smíðum ckeditor tilvik
# The session object requires your app to have a value set for the SECRET_KEY variable
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"  

admin = {
    "admino": {
        "username": "admino",
        "email": "jon@gmail.com",
        "password": "qwerty1",
        "bio": "Aðalgæinn á vefnum"
    }
}

@app.route("/", methods=["GET", "POST"])
def index():
    title = "Bókahillan"

    return render_template("index.html", title=title)

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username in admin:
            flash("Engin notandi er skráður með þetta nafn")
            return redirect(request.url)
        else:
            user = admin[username]  # user = dictionary
        if not password == user["password"]:
            flash("Rangt lykiorð")
            return redirect(request.url)
        else:
            # búum ti session
            session["USERNAME"] = user["username"]
            print(session)
            return redirect(url_for("profile"))
    return render_template("sign_in.html")

@app.route("/profile")
def profile():
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user = admin[username]  # dictionary
        flash("Velkomin/n " + user["username"])
        return render_template("profile.html", user=user)
    else:
        flash("Þú heur ekki aðgang að þessari síðu")
        return redirect(url_for("sign_in"))

@app.route("/form", methods = ['POST'])
def form():
    # formvinnsla 
    if request.method == 'POST':
        title = "Ný bók skráð"
        # sækjum gildin úr name breytum úr formi  
        kwargs = {
            "booktitle": request.form["title"],
            "isbn": request.form["isbn"],
            "author": request.form["author"],
            "timestamp": request.form["timestamp"]
        }    
        return render_template("index.html", **kwargs, title=title)
        # *args og **kwargs útskýrt: https://realpython.com/python-kwargs-and-args/

# Eyða session
@app.route("/sign-out")
def sign_out():
    session.pop("USERNAME", None)
    return redirect(url_for("sign_in"))

# 404 
@app.errorhandler(404)
def error(x):
    title = 'Vefsíðan finnst ekki'
    return render_template('error404.html', title=title)
# 405 
@app.errorhandler(405)
def error(ex):
    title = 'Aðferð ekki leyfð'
    return render_template('error405.html', title=title)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
