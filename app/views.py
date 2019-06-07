from flask import Flask, render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
import stripe

pub_key = 'pk_test_lGXe3xx2KfcxVMohkNhLQLzn00f0OXjTw8'
secret_key = 'sk_test_lKL5mpbIp5XQh3X750dAA8yr00laScgXRm'

stripe.api_key = secret_key

@app.route('/pay', methods = ['POST'])
def pay():
    if current_user.is_authenticated:
        customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

        charge = stripe.Charge.create(
            customer = customer.id,
            amount= 3999,
            currency ='usd',
            description= 'Premium User'
        )
        #######################
        # currently working to update user as premium_user after successful payment.
        print(current_user.get_id())
        update_this = User.query.filter_by(id=current_user.get_id()).first()
        if update_this:
            update_this.premium_user = True
            db.session.commit()
            flash('Congratulations, updated as premium_user!')

        #######################

        return 'Thanks for payment'


@app.route('/')
#@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('herokuapp'))
    return render_template('login.html', title='Sign In', form=form)

@login_required
@app.route('/herokuapp')
def herokuapp():
    return render_template('herokuapp.html')

@login_required
@app.route('/premium')
def premium():
    ######################################################################## changing 
    user = User.query.filter_by(id=current_user.get_id()).first()
    if user.premium_user is True:
        return render_template('herokuapp.html')
    else:
        return render_template('premium.html', pub_key = pub_key)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)