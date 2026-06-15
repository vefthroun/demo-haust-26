from flask import Flask,render_template,request
import urllib.request,json,random

app = Flask(__name__)
urlid = urllib.request.urlopen("http://api.tvmaze.com/shows")
data = json.loads(urlid.read().decode())

@app.route("/")
def index():
    listi = random.sample(data,20)
    return render_template("cool.html",l=listi)

@app.route("/new")
def new():
    urlid = urllib.request.urlopen("http://api.tvmaze.com/shows")
    data = json.loads(urlid.read().decode())
    # Filter out shows without a premiered date
    shows_with_date = [show for show in data if show.get("premiered")]
    # Sort by premiered date descending (newest first)
    sorted_shows = sorted(shows_with_date, key=lambda x: x["premiered"], reverse=True)
    # Take the top 20
    listi = sorted_shows[:20]
    return render_template("cool.html", l=listi)

@app.route("/shows/<int:id>")
def thattur(id):
    urlid = urllib.request.urlopen("http://api.tvmaze.com/shows/%s" %id)
    data = json.loads(urlid.read().decode())
    
    return render_template("show.html",d=data)

@app.route("/episodes/<int:id>")
def eps(id):
    urlid = urllib.request.urlopen("http://api.tvmaze.com/shows/%s/episodes" %id)
    data = json.loads(urlid.read().decode())
    
    return render_template("show.html",d=data)


@app.route("/leit")
def leit():
    return render_template("Leit.html")

@app.route("/lol", methods=['POST'])
def hmm():
    if request.method == "POST":
        eh = request.form.get("Fleit")
        eh = eh.replace(" ","%20")
        what = urllib.request.urlopen("https://api.tvmaze.com/search/shows?q={}".format(eh))
        gogn = json.loads(what.read().decode())
    return render_template("ThattaLeit.html",gogn=gogn)

@app.route("/genres/<fl>")
def flokkur(fl):
    urlid = urllib.request.urlopen("http://api.tvmaze.com/shows")
    data = json.loads(urlid.read().decode())
    return render_template("Genres.html",d=data,fl=fl)


@app.errorhandler(404)
def villa(e):
    return render_template("villur.html"),404

if __name__ == "__main__":
    app.run()
