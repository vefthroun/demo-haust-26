from app import app
from flask import render_template, request, session, redirect, url_for, flash

# login
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"  

'''from app import userlist
users = userlist'''

users = {
    "julian": {
        "username": "julian",
        "email": "julian@gmail.com",
        "password": "qwertyu",
        "bio": "Some guy from the internet"
    },
    "clarissa": {
        "username": "clarissa",
        "email": "clarissa@icloud.com",
        "password": "sweetpotato22",
        "bio": "Sweet potato is life"
    }
}

@app.route("/profile", methods = ["GET","POST"])
def profile():
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user = users[username]  # dictionary
        flash('þú ert innskráður')
        
        return render_template("profile.html", user=user)
    else:
        print("No username found in session")
        return redirect(url_for("sign_in"))

@app.route('/blogg_action', methods = ["POST"])
def blog():
    # formvinnsla 
    if request.method == 'POST':
        # sækjum key/value úr formi og setjum í breytu  
        kwargs = {
            "title": request.form["title"],
            "isbn": request.form["isbn"],
            "author": request.form["author"],
            "timestamp": request.form["timestamp"]
        }    
        #skilum kwargs í blogg session        
        bloggPost = kwargs
    #bætir bloggið aftast í blogg listanum í session
    session['blogg'].append(bloggPost)
    flash("Nýr bókartitill!")
    return redirect(url_for("index"))

# Eyða session
@app.route("/sign-out")
def sign_out():
    session.pop("USERNAME", None)
    flash("þú ert útskrifaður")
    return redirect(url_for("index"))
