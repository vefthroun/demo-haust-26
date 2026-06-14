from flask import Flask, render_template, request, session, redirect, url_for, flash
import urllib.request, json, random
import os # to generate secret key with operating system in flask app
from datetime import datetime # fyrir tímaskráningu pósta í spjallborði
from pprint import pprint  # pprint er í standard libary
from tinydb import TinyDB, Query

app = Flask(__name__)

# Secret key for session management
app.config["SECRET_KEY"] = os.urandom(16)
# Display the secret key and current time in console for debugging
#pprint(app.config["SECRET_KEY"])

#pprint({datetime.now()})

# --- Database Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, 'data'))
# Ensure DB folder exists & instantiate
os.makedirs(DB_PATH, exist_ok=True) 

POSTDB_FILE = os.path.join(DB_PATH, 'posts.json')

db_posts = TinyDB(POSTDB_FILE, indent=2, encoding='utf-8', ensure_ascii=False)

# Dummy admin user
admin = {
    "Addi": {
        "username": "Addi",
        "email": "addi@gmail.com",
        "password": "qwerty1",
        "bio": "Aðalgæinn á vefnum"
    }
}
# Forsíða með 20 handahófskenndum þáttum
@app.route("/", methods=["GET", "POST"])
def index():
    title = "TV MAZE"
    # Initial data load from TVmaze API
    urlid = urllib.request.urlopen("https://api.tvmaze.com/shows")
    data = json.loads(urlid.read().decode())
    # pprint(data)  # Skoðum gögnin í console
    # Veljum 20 handahófskennda þætti úr data
    listi = random.sample(data,20)
    return render_template("index.html", l=listi, title=title)

# Sjónvarpsþáttaröð valin með id frá index eða genres
@app.route("/shows/<int:id>")
def shows(id):
    urlid = urllib.request.urlopen("https://api.tvmaze.com/shows/%s" %id)
    data = json.loads(urlid.read().decode())
    # þættir í sjónvarpsseríu
    seasid = urllib.request.urlopen("https://api.tvmaze.com/shows/%s/seasons" %id)
    seasons = json.loads(seasid.read().decode())
    pprint(seasons)  # Skoðum gögnin í console
    # leikarar í þáttunum
    castid= urllib.request.urlopen("https://api.tvmaze.com/shows/%s/cast" %id)
    cast = json.loads(castid.read().decode())
    #pprint(cast)  # Skoðum gögnin í console
    return render_template("shows.html", d=data, s=seasons, c=cast, title=data["name"])

# Sjónvarpsþættir í sjónvarpsseríu valin með id frá shows
@app.route("/episodes/<int:id>")
def episodes(id):       
    urlid = urllib.request.urlopen("https://api.tvmaze.com/seasons/%s/episodes" %id)
    data = json.loads(urlid.read().decode())
    #pprint(data)  # Skoðum gögnin í console
    title = "Episodes"
    return render_template("episodes.html", d=data, title=title)

# sjónvarpsþáttur í valdri þáttaröð
@app.route("/seasons/<int:id>/episode/")
def episode(season_id, id):
    urlid = urllib.request.urlopen("https://api.tvmaze.com/seasons/%s/episodes/" %(id))
    data = json.loads(urlid.read().decode())
    #pprint(data)  # Skoðum gögnin í console
    title = "Episode: " + data["name"]
    return render_template("episode.html", d=data, title=title)

# Sjónvarpsþættir í völdum flokki - kvikmyndagrein.
@app.route("/genres/<fl>")
def flokkur(fl):
    urlid = urllib.request.urlopen("https://api.tvmaze.com/shows")
    data = json.loads(urlid.read().decode())
    title = "Genre: " + fl
    return render_template("genres.html", d=data, fl=fl, title=title)

# Leit að þáttum
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        if len(query.strip().split()) > 1: # ath. ef fleiri en eitt orð skrifað í leit
            flash("Please enter only one word in the search field.")
            return render_template("search.html")
        urlid = urllib.request.urlopen("https://api.tvmaze.com/search/shows?q=%s" %query)
        data = json.loads(urlid.read().decode())
        flash("Leit fyrir: " + query)
        return render_template("search_results.html", d=data)
    return render_template("search.html")

################## verkefni 3 + tinydb #####################

# pip install tinydb
# from tinydb import TinyDB, Query

# Skráning og innskráning og spjallborð
@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username in admin:
            flash("Engin notandi er skráður með þetta nafn")
            return redirect(request.url)
        else:
            user = admin[username]  # user = dictionary
        if not password == user["password"]:
            flash("Rangt lykiorð")
            return redirect(request.url)
        else:
            # búum ti session
            session["USERNAME"] = user["username"]
            print(session)
            return redirect(url_for("profile"))
    return render_template("sign_in.html")

@app.route("/profile")
def profile():
    title = "Spjallborð"
    # athugum hvort notandi sé skráður inn
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user = admin[username]  # dictionary
        # finnum alla pósta í db    
        posts = db_posts.all()
        posts = list(reversed(posts))  # Reverse the order
        #pprint(posts)
        flash("Velkomin/n " + user["username"])
        return render_template("profile.html", user=user, posts=posts, title=title)
    else:
        flash("Þú hefur ekki aðgang að þessari síðu")
        return redirect(url_for("sign_in"))

# nýr póstur
@app.route("/write", methods = ['POST'])
def create():
    # formvinnsla 
    if request.method == 'POST':
        # dagsetning og tími pósts bætt við færslu
        timestamp = datetime.now().strftime("%d/%m. %Y. Kl. %H:%M")
        # plus1 - Er notað til að búa til post_id
        plus1 = len(db_posts) +1
        # skráum póst í gagnagrunn
        title = request.form['titill']
        message = request.form['skilabod']
        db_posts.insert({
            "post_id":plus1,
            'titill': title,
            'skilabod': message,
            'username': session.get("USERNAME"),
            'timestamp': timestamp
        })
        return redirect(url_for('profile'))  

# Náum í póst með post_id 
@app.route('/update/<id>' , methods = ['GET','POST'])
def update(id):
    # athugum hvort notandi sé skráður inn
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user = admin[username]  # dictionary
    else:
        flash("Þú hefur ekki aðgang að þessari síðu")
        return redirect(url_for("sign_in"))
    js_post = db_posts.all()
    js_post = Query() # búum til Query object
    # Náum í póst með post_id   
    post = db_posts.get(js_post.post_id == int(id))
    #pprint(post)
    return render_template('update.html', post=post)
# Uppfæra póst í gagnagrunni
@app.route('/updatepost', methods = ['POST'])
def updatepost():
    if request.method == 'POST':
        post_id = request.form['post_id']
        title = request.form['titill']
        message = request.form['skilabod']  
        db_posts.update({'titill': title, 'skilabod': message}, Query().post_id == int(post_id))
        return redirect(url_for('profile'))
# Eyða pósti
@app.route('/delete/<id>' , methods = ['GET','POST'])
def delete(id): 
    js_post = db_posts.all()
    #pprint(js_post)
    js_post = Query() # búum til Query object
    db_posts.remove(js_post.post_id == int(id))
    return redirect(url_for('profile'))

# Eyða session
@app.route("/sign-out")
def sign_out():
    session.pop("USERNAME", None)
    return redirect(url_for("index"))

# 404 
@app.errorhandler(404)
def error(x):
    title = 'Vefsíðan finnst ekki'
    return render_template('error404.html', title=title)
# 405 
@app.errorhandler(405)
def er(ror):
    title = 'Aðferð ekki leyfð'
    return render_template('error405.html', title=title)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
