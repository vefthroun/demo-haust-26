from flask import Flask, render_template, request, session, redirect, url_for, flash
import urllib.request, json, random
from pprint import pprint  # pprint er í standard libary

app = Flask(__name__)

# Forsíða með 20 handahófskenndum þáttum
@app.route("/", methods=["GET", "POST"])
def index():
    title = "📺 TVmaze sjónvarpsþættir"
    # Initial data load from TVmaze API
    urlid = urllib.request.urlopen("https://api.tvmaze.com/shows")
    data = json.loads(urlid.read().decode())
    # pprint(data)  # Skoðum gögnin í console
    # Veljum 20 handahófskennda þætti úr data
    listi = random.sample(data,20)
    return render_template("index.html", listi=listi, title=title)

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

# 404 
@app.errorhandler(404)
def error(x):
    title = 'Vefsíðan finnst ekki'
    return render_template('error-40x.html', title=title)
# 405 
@app.errorhandler(405)
def erro(r):
    title = 'Aðferð ekki leyfð'
    return render_template('error-40x.html', title=title)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
