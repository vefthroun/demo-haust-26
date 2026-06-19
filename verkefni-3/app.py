from flask import Flask, render_template, request, redirect, url_for, session, flash
from tinydb import TinyDB, Query
import os                       # to generate secret key with operating system in flask app
from datetime import datetime   # fyrir tímaskráningu pósta í spjallborði
from pprint import pprint       # pprint er í standard libary

app = Flask(__name__)

# Secret key for session management
app.config["SECRET_KEY"] = os.urandom(16)
# Display the secret key and current time in console for debugging
pprint(app.config["SECRET_KEY"])

# --- Database Setup --- leiðin að db.json fundinn
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, 'data'))
# Ensure DB folder exists & instantiate
os.makedirs(DB_PATH, exist_ok=True) 

POSTDB_FILE = os.path.join(DB_PATH, 'db.json')

db = TinyDB(POSTDB_FILE, indent=2, encoding='utf-8', ensure_ascii=False)

# tengja db við appið
users_table = db.table('users')
posts_table = db.table('posts')
User = Query()
Post = Query()

# --- HJÁLPARFÖLL ---
def get_posts_with_users():
    all_posts = posts_table.all()
    for post in all_posts:
        # Nota author_id til að finna notanda [6, Conversation]
        user = users_table.get(doc_id=post['author_id'])
        post['username'] = user['username'] if user else "Óþekktur"
        post['id'] = post.doc_id # Ná í doc_id fyrir eyðingu/uppfærslu
    return all_posts

# Hvernig hægt er að uppfæra notanda (role:user) í admin
#users_table.update({'role': 'admin'}, Query().username == 'addiminn')

# --- RÁSIR (ROUTES) ---

@app.route('/')
def index():
    posts = get_posts_with_users()
    return render_template('index.html', posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') # Í alvöru kerfi þarf að hasha þetta!
        
        if not users_table.search(User.username == username):
            users_table.insert({'username': username, 'password': password, 'role': 'user'})
            flash("Nýskráning tókst! Skráðu þig inn.")
            return redirect(url_for('login'))
        flash("Notandanafn er frátekið.")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users_table.get((User.username == username) & (User.password == password))
        
        if user:
            session['user_id'] = user.doc_id # Vista ID í session
            session['username'] = user['username']
            return redirect(url_for('profile'))
        flash("Rangt notandanafn eða lykilorð.")
    return render_template('login.html')
'''
@app.route('/login', methods=['GET', 'POST']) # 1. Skilgreinum báðar aðferðir [1]
def login():
    # 2. Ef aðferðin er POST, þá vinnum við úr gögnunum úr forminu [2]
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Leitum að notanda í TinyDB (Conversation history)
        user = users_table.get((User.username == username) & (User.password == password))
        
        if user:
            session['user_id'] = user.doc_id # Vistum í session [4]
            
            # Skilyrði fyrir administrator eins og þú baðst um (Conversation history)
            if username == 'admin':
                session['role'] = 'admin'
            else:
                session['role'] = user.get('role', 'user')
                
            return redirect(url_for('profile')) # Sendum á prófíl eftir innskráningu [5]
        
        # Ef upplýsingar voru rangar
        flash("Rangt notandanafn eða lykilorð.") # Gefum feedback [6]
        return redirect(url_for('login'))

    # 3. Ef aðferðin er GET (notandi bara að opna síðuna), birtum við formið [7]
    return render_template('login.html')
'''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    # Sækja aðeins pósta þessa notanda [7, Conversation]
    my_posts = posts_table.search(Post.author_id == session['user_id'])
    for p in my_posts: p['id'] = p.doc_id
    return render_template('profile.html', posts=my_posts)

@app.route('/create_post', methods=['POST'])
def create_post():
    if 'user_id' in session:
        content = request.form.get('content')
        posts_table.insert({
            'content': content,
            'author_id': session['user_id'],
            'timestamp': datetime.now().strftime("%d. %m. %Y. Kl. %H:%M") # Íslensk dagsetning skráð í db
        })
    return redirect(url_for('profile'))

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post = posts_table.get(doc_id=post_id)
    if post and post['author_id'] == session.get('user_id'):
        posts_table.remove(doc_ids=[post_id])
        flash("Pósti eytt.")
    return redirect(url_for('profile'))

# Uppfærsla pósta

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # 1. Athugum hvort notandi sé innskráður
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 2. Sækjum póstinn úr TinyDB með doc_id
    post = posts_table.get(doc_id=post_id)

    # 3. Öryggisathugun: Má notandinn breyta þessum pósti?
    if not post or post['author_id'] != session['user_id']:
        flash("Þú getur aðeins breytt þínum eigin póstum!")
        return redirect(url_for('profile'))

    if request.method == 'POST':
        # 4. Sækjum nýja textann úr forminu
        new_content = request.form.get('content')
        
        # 5. Uppfærum póstinn í gagnagrunninum
        posts_table.update({'content': new_content}, doc_ids=[post_id])
        
        flash("Pósti hefur verið breytt!")
        return redirect(url_for('profile'))

    # Ef GET: Sýnum síðu með formi og gamla textanum
    return render_template('edit_post.html', post=post)

# stjórnborðið

@app.route('/admin_panel' , methods=['POST'])
def admin_panel():
    # 1. Öryggisathugun: Aðeins admin má sjá þessa síðu [57, Conversation]
    if session.get('role') != 'admin':
        flash("Aðgangur bannaður.")
        return redirect(url_for('index'))

    # 2. Sækja alla notendur úr users töflunni
    all_users = users_table.all()

    # 3. MIKILVÆGT: Bæta doc_id handvirkt inn í hvert dict [1, 3]
    # Annars virkar user.id ekki í HTML sniðmátinu
    for user in all_users:
        user['id'] = user.doc_id 

    return render_template('admin.html', users=all_users)

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

