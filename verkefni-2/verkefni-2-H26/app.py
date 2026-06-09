from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Einfaldur "gagnagrunnur" í minni
nemendur = {
    "1": {"nafn": "Jón Jónsson", "netfang": "jon@skoli.is"},
    "2": {"nafn": "Anna Önnu", "netfang": "anna@skoli.is"}
}

# Read

@app.route('/')
def index():
    # Birtir alla nemendur úr orðasafninu
    return render_template('index.html', nemendur=nemendur)

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

