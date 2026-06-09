from app import app
from flask import render_template, request, session, redirect, url_for, flash
import os
# random 16 bita session lykill 
app.secret_key = os.urandom(8)
print(app.secret_key)
users = {
    "Julian": {
        "username": "Julian",
        "email": "julian@gmail.com",
        "password": "1qwertyu",
        "bio": "Some guy from the internet"
    },
    "Clarissa": {
        "username": "Clarissa",
        "email": "clarissa@icloud.com",
        "password": "2qwertyu",
        "bio": "Sweet potato is life"
    }
}
#WTForm 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField #, EmailField, TextAreaField, IntegerField,HiddenField, DateField,
from wtforms.validators import InputRequired, Length #, AnyOf, DataRequired, 
# input reitir skilyrtir (Validators)
class SigninForm(FlaskForm):
    username = StringField('Notendanafn', validators=[InputRequired('Nafn vantar'), Length(min=5, max=12, message='Nafnið verður að vera 5 til 12 stafir.')])
    password = PasswordField('Lykilorð', validators=[InputRequired('Lykilorð vantar')]) 
    submit = SubmitField("Innskráning")

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    form = SigninForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username = form.username.data
            password = form.password.data
        if not username in users:
            flash("Innskráning tókst ekki, nafn ekki til")
            return redirect(request.url)
        else:
            user = users[username]  # user = dictionary
        if not password == user["password"]:
            flash("Rangt lykilorð, reyndu aftur")
            return redirect(request.url)
        else:
            # búum til session :)
            session["USERNAME"] = user["username"]
            print(session)
            return redirect(url_for("profile")) # user ok
    # GET /sign-in    
    return render_template('sign_in.html', form=form)