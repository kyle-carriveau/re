from flask import render_template, Blueprint

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def landing():
    return render_template("landing.html")