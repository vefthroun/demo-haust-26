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

# --- Database Setup --- leiðin að db fundinn
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, 'data'))
# Ensure DB folder exists & instantiate
os.makedirs(DB_PATH, exist_ok=True) 

POSTDB_FILE = os.path.join(DB_PATH, 'db.json')

db = TinyDB(POSTDB_FILE, indent=2, encoding='utf-8', ensure_ascii=False)

# tengja db við appið
#db = TinyDB('db.json', indent=2, encoding='utf-8', ensure_ascii=False)
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
            'timestamp': datetime.now().strftime("%d. %m. %Y.Kl.  %H:%M") # Íslensk dagsetning skrá í db
        })
    return redirect(url_for('profile'))

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post = posts_table.get(doc_id=post_id)
    if post and post['author_id'] == session.get('user_id'):
        posts_table.remove(doc_ids=[post_id])
        flash("Pósti eytt.")
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)

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

