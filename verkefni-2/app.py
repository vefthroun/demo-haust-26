from flask import Flask, render_template, request, redirect, url_for, session, flash
#from flask_ckeditor import CKEditor

app = Flask(__name__)

app.secret_key = 'Þe551_lyki11_Er_3rf1ður!' # Nauðsynlegt fyrir session

# CKEditor
#app.config['CKEDITOR_PKG_TYPE'] = 'basic'
#ckeditor = CKEditor(app)

# Einfaldur "gagnagrunnur" í vinnsluminni (cache) 
nemendur = {
    "1": {"nafn": "Jón Jónsson", "netfang": "jon@skoli.is"},
    "2": {"nafn": "Anna Önnudóttir", "netfang": "anna@skoli.is"}
}
skilabod = {
    "1": {"fyrirsogn": "Klúbbastarfið byrjað", 
          "postur": "Þetta eru fyrstu skilaboðin í skjóðunni", 
          "hofundur": "Jón Jónsson"},
    "2": {"fyrirsogn": "Hvað er á dagsskrá? ", 
          "postur": "Nú er þetta allt að smella saman 😉​", 
          "hofundur": "Anna Önnudóttir"}
}
administrator = {
    "123": {"nafn": "Addiminn", "netfang": "addi@skoli.is"}
}

# Read

@app.route('/')
def index():
    title = "Skilaboðaskjóðan"
    # Birtir alla nemendur úr orðasafninu og skilaboð
    return render_template('index.html', skilabod=skilabod, title=title)

# finnum nemanda eftir id og sendum á profile.html

@app.route('/nemandi/<id>')
def view_student(id):
    # Sækir ákveðinn nemanda með lykli (key)
    nemandi = nemendur.get(id)
    return render_template('profile.html', nemandi=nemandi)

#@app.route('/admin/<id>')
@app.route('/admin/<int:admin_id>')
#def view_admin(id):
def view_admin(admin_id):
    # Sækir admin með lykli (key)
    admin = administrator.get(id)
    nemar = nemendur
    return render_template('admin.html', nemendur=nemar, admin=admin)

# Create 
# (Nýskráning nemanda í klúbbinn)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Sækir fjölda nemenda úr nemandalistanum og bætir einum við (+ 1)
        nytt_id = str(len(nemendur) + 1) #nýtt id búið til 
        nafn = request.form.get('nafn')
        netfang = request.form.get('netfang')
        
        # Bætir nemanda í listann (sett í vinnsluminni núna en verður útfært í 3. verkefni)
        nemendur[nytt_id] = {"nafn": nafn, "netfang": netfang}
        return redirect(url_for('index'))
    return render_template('create_form.html')

# (Setjum nýjan póst í skilaboðasskjóðuna)

@app.route('/skrifa', methods=['GET', 'POST'])
def skrifa():
    if request.method == 'POST':
        # Sækir fjölda pósta úr skilabod listanum og bætir einum við (+ 1)
        post_id = str(len(skilabod) + 1) #nýtt post id búið til 
        fyrirsogn = request.form.get('fyrirsogn')
        postur = request.form.get('postur')
        hofundur = request.form.get('hofundur')

        # Bætir nýjum pósti í listann (sett í vinnsluminni núna en verður útfært betur í 3. verkefni)
        skilabod[post_id] = {"fyrirsogn": fyrirsogn, "postur": postur, "hofundur": hofundur}
        flash('Ný skilaboð!')
        return redirect(url_for('index'))
    return render_template('create_form.html')

# Update sett í verkefni 3

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        # Uppfærir gildi nemanda
        nemendur[id]['nafn'] = request.form.get('nafn')
        nemendur[id]['netfang'] = request.form.get('netfang')
        return redirect(url_for('index'))
    
    nemandi = nemendur.get(id)
    return render_template('update_form.html', nemandi=nemandi, id=id)

# Delete klárað í verkefni 3

@app.route('/delete/<id>')
def delete(id):
    # Fjarlægir nemanda með gefnu ID
    if id in nemendur:
        nemendur.pop(id)
    return redirect(url_for('view_admin'))

# login

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
    return render_template('index.html', skilabod=skilabod)

# admin login

@app.route('/admin', methods=['GET', 'POST'])
def get_admin():
    if request.method == 'POST':
        # Sækjum ID úr forminu með 'name' eigindinu
        admin_id = request.form.get('admin-id')
        #print(admin_id)
        # Athugum hvort lykillinn sé til í administrator
        if admin_id in administrator:
            # Geymum ID í session svo notandinn haldist innskráður á milli síðna
            session['admin_id'] = admin_id
            #print(admin_id)
            flash('Velkominn Addi minn!')
            #return redirect(url_for('view_admin'))
            return redirect(url_for('view_admin', admin_id=admin_id))
        else:
            # Ef ID finnst ekki, gefum við endurgjöf
            flash('Villa: Rangt admin-ID.')
            return redirect(url_for('index'))
    return render_template('index.html', skilabod=skilabod)

# logout

@app.route('/logout')
def logout():
    # Fjarlægir user_id úr session ef það er til staðar
    session.pop('user_id', None)
    
    # endurgjöf
    flash('Þú hefur verið skráð(ur) út.')
    
    # Senda notanda aftur á forsíðu eða innskráningarsíðu
    return redirect(url_for('index'))

# Profile - aðeins innskráður nemandi kemst þangað

@app.route('/profile')
def profile():

    # 1. Athuga hvort nemandi sé skráður inn í session
    user_id = session.get('user_id')
    
    # 2. Athuga hvort user_id sé í nemendalistanum
    if not user_id or user_id not in nemendur:
        # Ef ekki, senda notanda á forsíðu (aðgangur lokaður)
        flash('Þú ert ekki skráður í klúbbinn')
        return redirect(url_for('index'))
    
    # 3. Sækja gögn nemandans og birta síðuna
    nemandi = nemendur[user_id]
    #flash(f'Nemandinn {nemandi} hefur verið skráður!')
    return render_template('profile.html', nemandi=nemandi)

# 400 villur

@app.errorhandler(404)
def error4(x):
    title = '404 - villa, röng vefslóð'
    return render_template('error-40x.html', title=title)

@app.errorhandler(405)
def error5(x):
    title = '405 - aðgerð ekki leyfð'
    return render_template('error-40x.html', title=title)

if __name__ == '__main__':
    app.run(debug=True)

