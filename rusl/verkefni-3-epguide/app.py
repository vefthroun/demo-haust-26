import requests
from flask import Flask, render_template, request, redirect, url_for
from pprint import pprint

app = Flask(__name__)

# 1. Leiðrétt grunnslóð: Við notum aðal lénið sem grunn [1]
API_BASE_URL = "https://epguides.frecar.no"

@app.route('/')
def index():
    # 2. Ath: Ef /shows/ eða /popular skilar 404, þarftu að staðfesta 
    # réttan endapunkt í "REST API Reference" [3, Conversation].
    # Hér prófum við að sækja almennan lista (ef studdur):
    api_url = f"{API_BASE_URL}/shows/?page=1&page_size=20" 
    
    try:
        response = requests.get(api_url)
        shows = []

        if response.status_code == 200:
            # Sækjum JSON og tökum fyrstu 20 eins og beðið var um [56, Conversation]
            shows = response.json() #[:20]
            pprint(f"Sótti {len(shows)} þætti")
        else:
            pprint(f"Villa: API skilaði status {response.status_code}")
            
    except Exception as e:
        pprint(f"Tengingarvilla: {e}")
        shows = []
    pprint(shows)
    return render_template('index.html', shows=shows)

@app.route('/search')
def search():
    query = request.args.get('q')
    
    if not query:
        return redirect(url_for('index'))

    # 3. Lagað slóðasmíð: Nú verður slóðin https://epguides.frecar.no/show/{query} [2]
    search_url = f"{API_BASE_URL}/show/{query}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        show_data = response.json()
        # API-ið skilar oft einu orðasafni (dict) fyrir leit [2, 3]
        return render_template('results.html', show=show_data, query=query)
    else:
        # Ef þáttur finnst ekki (404), sýnum við enga niðurstöðu
        return render_template('results.html', show=None, query=query)

if __name__ == '__main__':
    app.run(debug=True)