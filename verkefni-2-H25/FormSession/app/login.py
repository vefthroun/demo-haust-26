from app import app
from flask import render_template, request, session, redirect, url_for, flash

# login
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"  

'''from app import userlist
users = userlist
print(users)'''

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
        "password": "2qwertyu",
        "bio": "Sweet potato is life"
    }
}

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username in users:
            flash("Username not found")
            return redirect(request.url)
        else:
            user = users[username]  # user = dictionary
        if not password == user["password"]:
            flash("Incorrect password")
            return redirect(request.url)
        else:
            # búum til session
            session["USERNAME"] = user["username"]
            print(session)
            return redirect(url_for("profile"))
    return render_template("sign_in.html")
