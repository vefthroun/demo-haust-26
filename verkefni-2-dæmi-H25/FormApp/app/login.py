from app import app
from flask import Flask, render_template, request

# login

@app.route("/login")
def login():
        return render_template("login.html")

# formvinnsla, vinnum með gögnin (e. input) frá formi
# skrifum method POST til að fá aðgang að post gögnum
@app.route("/login_process", methods = ['POST'])
def result():
# sækjum streng/gildi úr name breytum frá formi
        name = request.form.get("user_name")  # request.form.get() skilar streng
        email =  request.form.get("user_email")
        print(name)
        return render_template("login_result.html", name=name, email=email)


'''        if request.method == 'POST':
                # sækjum streng/gildi úr name breytum frá formi
                name = request.form.get("user_name")  # request.form.get() skilar streng
                email =  request.form.get("user_email")
                print(name)
        return render_template("login_result.html", name=name, email=email)'''

