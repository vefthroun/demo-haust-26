import requests
from flask import render_template

@app.route('/shows')
def shows():
    # Sækjum gögn frá Epguides API (þetta er dæmi um slóð)
    response = requests.get('https://epguides.frecar.no/shows/')
    all_shows = response.json()
    
    # Veljum aðeins fyrstu 20 þættina úr listanum
    top_20_shows = all_shows[:20]
    
    return render_template('shows.html', shows=top_20_shows)

