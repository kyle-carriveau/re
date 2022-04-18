from crypt import methods
from flask import render_template, Blueprint, render_template_string, request, redirect, url_for
from .models import User, Portfolio, Tenant, Property, Unit
from . import db 
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

'''
TOP ROUTES

BOTTOM NON-ROUTE FUNCTIONS

'''
views = Blueprint('views', __name__)

@views.route('/')
def landing():
    return render_template("landing.html")

@views.route('/home')
@login_required
def home():
    return render_template("profile/dashboard.html", user=current_user)

@views.route('/profile')
@login_required
def profile():
    return render_template("profile/profile.html", user=current_user, properties=get_properties(), tenants=get_tenants()) 

@views.route('/settings')
@login_required
def settings():
    return render_template("profile/settings.html", user=current_user)

@views.route('/portfolios', methods=['GET', 'POST']) 
@login_required 
def portfolios():
    if request.method == "POST":
        name = request.form.get('portfolio_name')
        new_portfolio = Portfolio(name=name, owner=current_user.id)
        db.session.add(new_portfolio)
        db.session.commit()
        return redirect(url_for('views.portfolios', user=current_user))
    return render_template("profile/portfolios.html", user=current_user, portfolios=get_portfolios())

@views.route('/properties', methods=['GET', 'POST'])
@login_required
def properties():
    if request.method == "POST":
        name = request.form.get('property_name')
        portfolio = request.form.get('portfolio')
        new_property = Property(name=name, owner=current_user.id, portfolio=portfolio)
        db.session.add(new_property)
        db.session.commit()
        return redirect(url_for("views.properties", user=current_user, properties=get_properties(), portfolios=get_portfolios()))
    return render_template("profile/properties.html", user=current_user, properties=get_properties(), portfolios=get_portfolios())

@views.route('/property/<int:id>', methods=['GET', 'POST'])
@login_required
def property(id):
    property = Property.query.filter_by(id=id, owner=current_user.id).first()
    return render_template("profile/property.html", user=current_user, property=property, units=get_units(property.id))

@views.route('/edit_property/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_property(id):
    property = db.session.query(Property).filter_by(id=id, owner=current_user.id).first()
    #property = Property.query.filter_by(id=id, owner=current_user.id).first()
    if request.method == "POST":
        property.name = request.form.get('name')
        property.bedrooms = request.form.get('bedrooms')
        property.bathrooms = request.form.get('bathrooms')
        property.type = request.form.get('type')
        property.units = request.form.get('units')
        property.address = request.form.get('address')
        property.city = request.form.get('city')
        property.state = request.form.get('state')
        property.zip_code = request.form.get('zip_code')
        property.rent = request.form.get('rent')

        db.session.commit()
        return redirect(url_for('views.property', id=id))

    return render_template("profile/edit_property.html", user=current_user, property=property, states=get_states())

@views.route('/create_unit/<int:id>', methods=['GET', 'POST'])
@login_required
def create_unit(id):
    properties = Property.query.filter_by(owner=current_user.id).all()
    if request.method == "POST":
        name = request.form.get('name')
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        sqft = request.form.get('sqft')
        property = request.form.get('property')
        rent = request.form.get('rent')
        
        new_unit = Unit(name=name, bedrooms=bedrooms, bathrooms=bathrooms, sqft=sqft, property=property, rent=rent)
        db.session.add(new_unit)
        db.session.commit()
        return redirect(url_for('views.property', id=id))
        
    return render_template("profile/create_unit.html", user=current_user, properties=properties)

@views.route('/tenants', methods=['GET', 'POST'])
@login_required
def tenants():
    return render_template("profile/tenants.html", user=current_user, tenants=get_tenants())

@views.route('/create_tenant', methods=['GET', 'POST'])
@login_required
def create_tenant():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        property = request.form.get('property')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')

        new_tenant = Tenant(first_name=first_name, last_name=last_name, email=email, phone=phone, property=property, address=address, city=city, state=state, zip_code=zip_code)

        db.session.add(new_tenant)
        db.session.commit()

    return render_template("profile/create_tenant.html", user=current_user, properties=get_properties(), states=get_states())

@views.route('/tenant', methods=['GET', 'POST'])
@login_required
def tenant():
    return render_template("profile/tenant.html", user=current_user)

@views.route('/create')
def check_user():
    user = User.query.filter_by(email="kyle.carriveau@gmail.com").first()
    if user:
        login_user(user, remember=True)
    else:
        new_user = User(first_name="Kyle", last_name="Carriveau", email="kyle.carriveau@gmail.com", password=generate_password_hash("password", method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
    return redirect(url_for('views.home'))

'''

NON ROUTE FUNCTIONS

'''

def get_tenants():
    tenants = Tenant.query.filter_by(landlord=current_user.id).order_by(Tenant.last_name.asc()).all()
    return tenants

def get_tenant(id):
    tenant = Tenant.query.filter_by(id=id).first()
    return tenant

def get_portfolios():
    portfolios = Portfolio.query.filter_by(owner=current_user.id).order_by(Portfolio.name.asc()).all()
    return portfolios

def get_properties():
    properties = Property.query.filter_by(owner=current_user.id).order_by(Property.name.asc()).all()
    return properties

def get_units(id):
    units = Unit.query.filter_by(owner=current_user.id, property=id).order_by(Unit.name.asc()).all()
    return units

def get_states():
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI', 'WA', 'WV', 'WI', 'WY']
    return states