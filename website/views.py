from flask import render_template, Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def landing():
    return render_template("landing.html")

@views.route('/login')
def login():
    return render_template("auth/login.html")