from app import app
from flask import render_template, request

@app.errorhandler(404)
def pagenotfound(e404):
    title="Vefsíðan finnst ekki - 404"
    return render_template("error.html", title=title), 404

@app.errorhandler(405)
def methodnotalowed(e405):
    title="Aðferð ekki leyfð - 405"
    return render_template("error.html", title=title), 405

# Server error
@app.errorhandler(500)
def servernotfound(error):
    title="error 500 server virkar ekki"
    return render_template("error.html", title=title), 500