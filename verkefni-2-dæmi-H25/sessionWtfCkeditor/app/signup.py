from app import app
from flask import render_template #request, session, redirect, url_for, flash
import os
# random 8 bita session lykill 
app.secret_key = os.urandom(8)

#WTForm 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField  #?EmailField?, IntegerField, HiddenField, DateField,
from wtforms.validators import InputRequired, Length, EqualTo, DataRequired, Email #, AnyOf

# input reitir skilyrtir (validators) 
class SignupForm(FlaskForm):
    usname = StringField('Notendanafn', validators=[InputRequired('Nafn vantar'), 
					Length(min=2, max=25, message='Nafn á að vera að lágmarki 2 stafir og ekki fleiri en 25.')])
    email = StringField('Tölvupóstfang', validators = [InputRequired('Tölvupóstfang vantar'),
					DataRequired(), Email('Tölvupóstfang er ekki rétt skráð')])
    psword = PasswordField('Lykilorð', validators=[InputRequired('Lykilorð vantar'), 
					Length(min=7, message='Lykilorð á að vera að lágmarki 7 stafir.'), 
					EqualTo('pscheck', message='Lykilorðin eru ekki eins')]) 
    pscheck = PasswordField('Skráðu lykilorðið aftur') 
    submit = SubmitField("Nýskráning")

@app.route("/sign-up", methods = ['POST', 'GET'])
def sign_up():
	sign = SignupForm()
	if sign.validate_on_submit():
		usname = sign.usname.data
		email = sign.email.data
		psword = sign.psword.data
		pscheck = sign.pscheck.data
		print(sign) # ? 4 verkefni, hvernig á að skrifa notanda í json skrá ?
		sign = 'Nýskráning tókst, eða þannig sko ...' 
		return render_template("signup_result.html", sign=sign)
	else:
		return render_template('sign_up.html', sign=sign)

# athugið að email_validator verður að vera með
## pip install email_validator
