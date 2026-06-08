from flask import Flask, render_template

app = Flask(__name__)

company = {
    'company':'PY Pizzeria',
    'email': 'pypizzur@tskoli.is',
    'school': 'VEFÞ2VFC5AU, tölvubraut Tækniskólans'
}
# Dæmi dictionary í list.

menu =  [
        {
            "id": 0,
            "nafn": "El Peppó Xtra",
            "mynd": "Pepperoni_pizza.jpg",
            "verd":1600,
            "álegg":["Xtra pepperóni", "Xtra ostur", "Xtra Sósa"],
            "flokkur":"keto"
        },
        {
            "id": 1,
            "nafn": "El Vegó",
            "mynd": "Vegan_pizza.jpg",
            "verd":1400,
            "álegg":["Paprika", "Laukur", "Ananas"],
            "flokkur":"vegan"
        },
        {
            "id": 2,
            "nafn": "Pizza MOI",
            "mynd": "Pizza_Moi.jpg",
            "verd":2000,
            "álegg":["Banani", "Ananas", "Lárviðarlauf"],
            "flokkur":"vegan"
        },
        {
            "id": 3,
            "nafn": "El Logos",
            "mynd": "El_Logos.jpg",
            "verd":1500,
            "álegg":["Spicy Pepperoni", "Chilli Pepper", "Hot Sauce", "Laukur"],
            "flokkur":"sterk"
        },
        {
            "id": 4,
            "nafn": "Pizza Domo",
            "mynd": "Pizza_Domo.jpg",
            "verd":2500,
            "álegg":["Nautahakk", "Paprika", "Laukur"],
            "flokkur":"keto"
        },
        {
            "id": 5,
            "nafn": "El Grande",
            "mynd": "El_Grande.jpg",
            "verd":3000,
            "álegg":["Pepperoni", "Skinka", "Nautahakk", "Paprika", "Laukur"],
            "flokkur":"keto"
        }
    ]


@app.route('/')
def index():
    title= 'Py Pizzeria'
    return render_template('index.html', title=title, menu=menu, co=company)

# 1 pizza valin
@app.route('/pizzaval/<id>')
def pizza(id):
    title='Þú hefur valið'
    id = menu[int(id)]
    print(id)
    return render_template("pizzaval.html", pi=id, title=title, co=company)

# pizza flokkur
@app.route('/flokkur/<tegund>')
def flokkur(tegund):
    title='Áleggstegund'
    print(tegund) 
    return render_template("flokkur.html", menu=menu, title=title, tegund=tegund, co=company)

@app.route('/titill')
def test():
    return render_template('test.html', co=company)
# 404 villa
@app.errorhandler(404)
def error(x):
    title = '404 - Pizzan finnst ekki'
    return render_template('error-404.html', title=title, co=company)

if __name__ == '__main__':
    app.run(debug=True)
