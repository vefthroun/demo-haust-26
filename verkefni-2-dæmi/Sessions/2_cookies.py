from flask import Flask, render_template, request, make_response
app = Flask(__name__)


# let's set a cookie with the key of flavor and the value of chocolate chip:
@app.route("/")
@app.route("/cookies")
def cookies():

    # By using make_response() we can build and modify our request ahead of sending it.
    resp = make_response("Cookies 2")
    
    # búum til cookie ásamt parametrum með set_cookie fallinu
    # resp.set_cookie("key", value="value", max_age=0, expires=0, path='/', domain=None, secure=False, httponly=False, samesite=None) 
    # https://flask.palletsprojects.com/en/3.0.x/api/#flask.Response.set_cookie
    resp.set_cookie(
        "flavor2", 
        value="chocolate chip",
        max_age=5,  # expires in 10 seconds
    ) 

    return resp     # skilar "Cookies" streng í vafrann


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

"""
Cookies eru í vaframinni 
1. Opnaðu Developer tools í vafra og veldu Application (chrome). 
2. Smelltu á Cookies og skoðaðu upplýsingarnar. 
3. Hinkraðu í 10 sekúnudur, flavor eyðist þá.

"""
