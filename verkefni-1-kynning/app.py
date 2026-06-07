from flask import Flask, render_template

app = Flask(__name__)

# dict listi [{}]
áfangaval = [
    {   "id":0,
        "áfangi": "GRU2UX05BU", 
        "heiti": "Stafræn hönnun",
        "lýsing":"Notuð eru margmiðlunar- og hreyfimyndaforrit til að útbúa grafískt margmiðlunarefni. Farið er í helstu atriði sem snúa að vinnslu á mynd-, hljóð- og grafísku efni fyrir vef, sjónvarp og útvarp.",
        "mynd":"AE.png"
    },    
    {   "id":1,
        "áfangi": "VEFÞ1VG05AU", 
        "heiti": "Vefgrunnur",
        "lýsing":"VEFÞ1 er grunnáfangi í vefsíðugerð og mikilvæg undirstaða undir vefforritun. Farið er í grunnatriði viðmótshönnunar og áhersla er lögð á HTML ritun, CSS stílsíður og myndvinnslu. Hver þessara þátta er tekinn sérstaklega fyrir og sýnt er hvernig samspil þeirra stuðlar að vandaðri framsetningu.",
        "mynd":"vef1vg.png"
    },    
    {    "id":2,
         "áfangi": "VEFÞ2VH05AU", 
         "heiti": "Vefhönnun",
         "lýsing":"Farið er í að hanna vef sem er sveigjanlegur (Responsive Web Design), oft nefndir snjallvefir. Til þess notum við aðalega ívafsmál (HTML) og stílsnið (CSS3). Hvernig er hægt að lífga upp á vefsíður með því að láta form bregðast vali notenda. Skoðað er hvernig hægt er að nota vefumsjónartól til að leggja grunn að góðum vef.",
        "mynd":"vef2vh.jpg"
    },
    {   "id":3,
        "áfangi": "VEFÞ2VF05BU2",
        "heiti": "Vefforritun",
        "lýsing":"Í áfanganum eru grunnatriði vefforritunar kynnt. Farið er í miðlara/biðlara uppbyggingu vefsíðna, samskipti þeirra og hlutverk hvers hluta. Nemendur vinna að smíði vefja með miðlaramáli. Lögð er áhersla á málfræði og endurnýtni á kóða í gerð vefja.",
        "mynd":"vef2vf.jpg"
    }]

@app.route('/')
def index():
    title = "👋  Kynning"
    intro = "Guðmundur heiti ég og kenni á fjölmiðla- og tölvubraut Upplýsingatækniskólans. Áfangarnir sem ég kenni í Upplýsingatækniskólanum eru meðal annars:"
    áfangar = {  
            0:"GRU2UX05BU",
            1:"VEFÞ1VG05AU",
            2:"VEFÞ2VH05AU",
            3:"VEFÞ2VF05BU"}
    
    # sendum dictionary (áfangar) og breytuna (title) í template
    return render_template('index.html', title=title, intro=intro, áfangar=áfangar)

@app.route('/afangar/<int:id>')
def afangar(id):
   title="✨ Áfangaval"
   id = áfangaval[int(id)] # ATH! hér er route id notað til að finna sama id í dict listanum 
   #print(id['mynd'])
   return render_template('afangi.html', id=id, title=title)

# Client error
# This tells Flask that the status code of that page should be 404 which means not found. 
@app.errorhandler(404)
def pagenotfound(error):
    title = "Vefsíðan finnst ekki ( http villa 404 )"
    return render_template('error.html', title=title)

# Server error
@app.errorhandler(500)
def servernotfound(error):
    return "Server is down!", 500

if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)  
    