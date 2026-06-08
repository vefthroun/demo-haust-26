from app import app
from flask import render_template, request, session, redirect, url_for, flash
# https://flask-ckeditor.readthedocs.io/en/latest/basic.html#installation
import os
# session lykill
app.secret_key = os.urandom(8)

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
from flask_ckeditor import CKEditor
from flask_ckeditor import CKEditorField
#WTForm 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField #, PasswordField, EmailField, IntegerField,HiddenField, DateField,
from wtforms.validators import InputRequired, Length #, AnyOf, DataRequired, 

# input reitir skilyrtir (Validators)
class BF(FlaskForm):
    titill = StringField('Titill', validators=[InputRequired('Bókartitil vantar'), Length(min=4, max=25, message='Titilinn verður að vera 4 til 25 stafir.')])
    isbn = IntegerField('ISBN númer', validators=[InputRequired('ISBN vantar'), Length(min=13, max=13, message='ISBN númer er 13 tölustafir.')])
    lysing = TextAreaField('Innihaldslýsing', validators=[InputRequired('Lýsingu vantar'), Length(min=20, max=200, message='Hafðu lýsinguna innan skynsamlegra marka.')]) 
    author = StringField('Höfundur', validators=[InputRequired('Höfund vantar')])
    submit = SubmitField("Senda póst")

ckeditor = CKEditor(app)  # fyrir jinja template

@app.route("/profile", methods = ["GET","POST"])
def profile():
    form = BF()
    title="Bókaskráning"
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user = users[username]  # dictionary
        flash('þú ert innskráður')
        return render_template("profile.html", user=user, title=title, form=form)
    else:
        flash("Þú verður að skrá þig inn")
        return redirect(url_for("sign_in"))

@app.route('/blogg_action', methods = ["POST"])
def blog():
    form = BF() # ? WTForm validators tjékka á kwargs/session/bloggPost :o ?
    if request.method == 'POST':
        # sækjum key/value úr formi og setjum í breytu  
        kwargs = {
            "titill": request.form["titill"],
            "isbn": request.form["isbn"],
            "lysing": request.form["lysing"],
            "author": request.form["author"],
            #"timestamp": request.form["timestamp"]
        }    
        #skilum kwargs í blogg session        
        bloggPost = kwargs
        print(bloggPost)
        #bætir bloggið aftast í blogg listanum í session
        session['blogg'].append(bloggPost)
        flash("Ný bók hefur verið sett í hilluna :)")
    return redirect(url_for("index"))

# Eyða session
@app.route("/sign-out")
def sign_out():
    session.pop("USERNAME", None)
    flash("Útskráning tókst.")
    return redirect(url_for("index"))

''' ??? if form.validate_on_submit():
            titill = form.titill.data
            isbn = form.isbn.data
            lysing = form.lysing.data
            author = form.author.data'''