from app import app
from flask import Flask, render_template, request  

# https://www.tutorialspoint.com/flask/flask_sending_form_data_to_template.htm

# signup -nýskráning
@app.route("/signup")
def signup():
        return render_template("signup.html")

# formvinnsla
@app.route("/signup_process", methods = ['POST'])
def register():
        if request.method == 'POST':
            # sækjum streng/gildi úr name breytum frá formi 
            result = request.form  # request.form skilar dictionary 
        return render_template("signup_result.html", result=result)

