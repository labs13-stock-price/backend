from flask import Flask, render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, ContactForm
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from app.models import User, OAuth
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
import stripe
from config import Config
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound

#Password RESET
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email, Message, mail

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
google_blueprint = make_google_blueprint(client_id = Config.GOOGLE_CLIENT_ID,
                                        client_secret= Config.GOOGLE_CLIENT_SECRET,
                                        scope=["email", "profile", "openid"],
                                        redirect_to='google_url')
app.register_blueprint(google_blueprint, url_prefix="/google_login")

@app.route('/google_url')
def google_url():
    print("INSIDE GOOGLE LINK ROUTE.............")
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/plus/v1/people/me")
    print("GOOGLE AUTHORISATION IN >>>>>>....... : ",resp)
    assert resp.ok, resp.text
    print("GOOGLE C  : ",resp.json()['name']["givenName"])

    ####### Google-user-database update
    google_user = resp.json()['name']["givenName"]
    query = User.query.filter_by(username = google_user)

    try:
        user = query.one()
    except NoResultFound:
        user = User(username = google_user)
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
        return redirect(url_for('herokuapp'))

################################ Github-Login route ############################################# 
github_blueprint = make_github_blueprint(client_id = Config.GITHUB_CLIENT_ID, 
                                         client_secret = Config.GITHUB_CLIENT_SECRET,
                                         redirect_to='github_url')
app.register_blueprint(github_blueprint, url_prefix="/github_login")
github_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)
@app.route('/github_url')
def github_url():
    print("INSIDE GITHUB LINK ROUTE.............")     
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    print("GITHUB AUTHORISATION IN github_login route....... : ",resp)
    assert resp.ok
    print(">>>>>>>>>>>>>>>>>>>>>>>>>> : ",resp.json()) 

    github_user = resp.json()["login"]
    query = User.query.filter_by(username = github_user)

    try:
        user = query.one()
    except NoResultFound:
        user = User(username = github_user)
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
        return redirect(url_for('herokuapp'))


############################# Twitter-Login route ############################################
twitter_blueprint = make_twitter_blueprint(api_key = Config.TWITTER_API_KEY,
                                           api_secret= Config.TWITTER_API_SECRET,
                                           redirect_to='twitter_url')
app.register_blueprint(twitter_blueprint, url_prefix="/twitter_login")

@app.route('/twitter_url')
def twitter_url():
    print("INSIDE TWITTER LINK ROUTE.............")
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get('account/settings.json')
    print("TWITTER AUTHORISATION IN >>>>>>....... : ",resp)
    assert resp.ok
    print("TWITTER C  : ",resp.json()['screen_name'])

    twitter_user = resp.json()['screen_name']
    query = User.query.filter_by(username = twitter_user)

    try:
        user = query.one()
    except NoResultFound:
        user = User(username = twitter_user)
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
        return redirect(url_for('herokuapp'))
 
###################### Contact route ###################################
@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form = form)
        else:
            msg = Message(form.subject.data, sender = 'contact@example.com', recipients = [Config.MAIL_USERNAME])
            
            msg.body = """
                        From: %s <%s> %s
                       """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('contact.html', success=True)

    elif request.method == 'GET':
        return render_template('contact.html', form = form)




