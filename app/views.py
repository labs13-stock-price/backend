from flask import Flask, render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from app.models import User, OAuth
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
import stripe
from config import Config
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage

#Password RESET
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    print("############### RESET PASSWORD REQUEST   ",form.email.data)
    if form.validate_on_submit():
        print("EMAIL FOR RESETING PASSWORD ... :  ",form.email.data)
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user) 
            print("EMAIL FOR RESETING PASSWORD ... :  ",form.email.data)
            flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
######################## BASIC ROUTE '/' AND '/INDEX'##############################
@app.route('/')
@app.route('/index')
def index():
    print("HOME PAGE..............")
    return render_template('index.html', title='Home Page')

########################## REGISTER ###########################
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

######################### LOGIN ###############################
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

######################### LOGOUT ##############################
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


####################### Route for logged-in user to see basic stock-price-info
@login_required
@app.route('/herokuapp')
def herokuapp():
    return render_template('herokuapp.html')

####################### Route for logged-in user to update as premium-user
@login_required
@app.route('/premium')
def premium():
    user = User.query.filter_by(id=current_user.get_id()).first()
    if user.premium_user is True:
        return render_template('premium_already.html', current_user = user.username)
    else:
        return render_template('premium_update_form.html', pub_key = pub_key)

######################### STRIPE-PAYMENT-ACCEPT ROUTE to accept payment to update free-user to premium-user

pub_key = Config.STRIPE_PUB_KEY
secret_key = Config.STRIPE_SECRET_KEY
stripe.api_key = secret_key

@login_required
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
        
        print(current_user.get_id())
        update_this = User.query.filter_by(id=current_user.get_id()).first()
        if update_this:
            update_this.premium_user = True
            db.session.commit()
            #flash('Congratulations, updated as premium_user!')

        return render_template('premium_response.html', current_user = update_this.username)

############################### Google-Login route ##############################################
google_blueprint = make_google_blueprint(
                                        client_id = Config.GITHUB_CLIENT_ID,
                                        client_secret= Config.GITHUB_CLIENT_SECRET)
app.register_blueprint(google_blueprint, url_prefix="/google.login")

@app.route('/google.login')
def google_login():
    print("INSIDE GOOGLE LINK ROUTE.............")

    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["emails"][0]["value"])



################################ Github-Login route ############################################# 
github_blueprint = make_github_blueprint(client_id = Config.GITHUB_CLIENT_ID, 
                                         client_secret = Config.GITHUB_CLIENT_SECRET)
app.register_blueprint(github_blueprint, url_prefix="/github.login")

@app.route('/github_login')
def github_login():
    print("INSIDE GITHUB LINK ROUTE.............")     
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    print("GITHUB AUTHORISATION ....... : ",resp)
    assert resp.ok
    return "You are @{login} on GitHub".format(login=resp.json()["login"])

################################## GITHUB REDIRECT-URI #############
github_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)
@app.route('/ld/github/authorized')
def github2():
    return redirect(url_for('herokuapp'))











################################ Twitter-Login route ############################################
############################### FORGOT-Password route ##############################################
############################### NEW---Password-setting###########################################
 



