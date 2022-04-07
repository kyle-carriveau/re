from flask import Flask
from os import path
#from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(session_options={"autoflush": False})


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'keyissecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://re-user-db-connect:B0nehe@d1@turing-variety-344019:us-west4:re-db?driver=ODBC+Driver+17+for+SQL+Server'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    #create_database(app)

    
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    #from .auth import auth

    '''
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    '''
    return app

'''
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('created database')
'''