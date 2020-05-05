from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, GetRestaurants
from flaskblog.models import User, Restaurants
from flask_login import login_user, current_user, logout_user, login_required
import requests
import json
import time

business_types = ["restaurant"]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/restaurants", methods=['GET', 'POST'])
@login_required
def get_restaurants():
    form = GetRestaurants()
    if form.validate_on_submit():
        post = Restaurants(name=form.title.data, latitude=form.latitude.data, longitude=form.longitude.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your search is completed!', 'success')
        url = "https://tripadvisor1.p.rapidapi.com/restaurants/list-by-latlng"
        querystring = {"limit": "30", "currency": "USD", "distance": "2", "lunit": "km", "lang": "en_US",
                       "latitude": form.latitude.data, "longitude": form.longitude.data}
        headers = {
            'x-rapidapi-host': "tripadvisor1.p.rapidapi.com",
            'x-rapidapi-key': "8f2c80d858msh122851999070f9bp18d761jsn14f5b382b22f"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)

        return str(response.text)
    return render_template('getRestaurants.html', title='Your Restaurants', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


