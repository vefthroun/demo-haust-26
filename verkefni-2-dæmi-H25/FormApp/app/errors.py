from app import app
from flask import Flask, render_template

@app.errorhandler(404)
def error(e404):
    title = '404 - vefsíðan finnst ekki'
    return render_template('errors.html', title=title)

@app.errorhandler(405)
def error(e405):
    title = '405 - Aðferð ekki leyfð'
    return render_template('errors.html', title=title)
