from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_ckeditor import CKEditor

app = Flask(__name__)

app.secret_key = 'Þess1_lyki11_Er_3rf1ður!' # Nauðsynlegt fyrir session

# CKEditor
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)

# Einfaldur "gagnagrunnur" í minni
nemendur = {
    "1": {"nafn": "Jón Jónsson", "netfang": "jon@skoli.is"},
    "2": {"nafn": "Anna Önnudóttir", "netfang": "anna@skoli.is"}
}

# Read

@app.route('/')
def index():
    title = "Forsíða"
    # Birtir alla nemendur úr orðasafninu
    return render_template('index.html', nemendur=nemendur, title=title)

@app.route('/nemandi/<id>')
def view_student(id):
    # Sækir ákveðinn nemanda með lykli (key)
    nemandi = nemendur.get(id)
    return render_template('profile.html', nemandi=nemandi)

# Create

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Sækir gögn úr formi
        nytt_id = str(len(nemendur) + 1)
        nafn = request.form.get('nafn')
        netfang = request.form.get('netfang')
        
        # Bætir við í orðasafnið
        nemendur[nytt_id] = {"nafn": nafn, "netfang": netfang}
        return redirect(url_for('index'))
    return render_template('create_form.html')

# Update

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        # Uppfærir gildi nemanda
        nemendur[id]['nafn'] = request.form.get('nafn')
        nemendur[id]['netfang'] = request.form.get('netfang')
        return redirect(url_for('index'))
    
    nemandi = nemendur.get(id)
    return render_template('update_form.html', nemandi=nemandi, id=id)

# Delete

@app.route('/delete/<id>')
def delete(id):
    # Fjarlægir nemanda með gefnu ID
    if id in nemendur:
        nemendur.pop(id)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Sækjum ID úr forminu með 'name' eigindinu
        user_id = request.form.get('user_id')
        
        # Athugum hvort lykillinn sé til í nemenda-dictionary
        if user_id in nemendur:
            # Geymum ID í session svo notandinn haldist innskráður á milli síðna
            session['user_id'] = user_id
            flash('Innskráning tókst!')
            return redirect(url_for('profile'))
        else:
            # Ef ID finnst ekki, gefum við endurgjöf
            flash('Villa: Rangt nemenda-ID.')
            return redirect(url_for('index'))
            
    return render_template('index.html')

# logout

@app.route('/logout')
def logout():
    # Fjarlægir user_id úr session ef það er til staðar
    session.pop('user_id', None)
    
    # Gefa notanda endurgjöf
    flash('Þú hefur verið skráð(ur) út.')
    
    # Senda notanda aftur á forsíðu eða innskráningarsíðu
    return redirect(url_for('index'))

# Profile

@app.route('/profile')
def profile():
    # 1. Athuga hvort notandi sé skráður inn í session
    user_id = session.get('user_id')
    
    # 2. Athuga hvort user_id sé í nemendalistanum
    if not user_id or user_id not in nemendur:
        # Ef ekki, senda notanda á forsíðu (aðgangur lokaður)
        flash('Þú ert ekki skráður í vefáfangann')
        return redirect(url_for('index'))
    
    # 3. Sækja gögn nemandans og birta síðuna
    nemandi = nemendur[user_id]
    #flash(f'Nemandinn {nemandi} hefur verið skráður!')
    return render_template('profile.html', nemandi=nemandi)


# 404 villa

@app.errorhandler(404)
def error(x):
    title = '404 - villa, röng vefslóð'
    return render_template('error-404.html', title=title)

if __name__ == '__main__':
    app.run(debug=True)

