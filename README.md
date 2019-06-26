# Stock-price(Back-end and Front-end)

Back-end as well as Front-end repo for labs13-Stock-price

# API Documentation

#### App delpoyed at [HEROKU](https://stock-price-stripe.herokuapp.com/) <br>

## Getting started
The complete application is build with Flask which is a microframework for Python based on Werkzeug, Jinja 2. 
<br>

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

To get the server running locally:

- Clone this repo <br>
$ git clone https://github.com/labs13-stock-price/backend.git <br>
$ cd backend <br>

- Install the dependencies: <br>
$ pip install -r requirements.txt <br>

- Run the development server: <br>
$ python run.py <br>

- Navigate to http://localhost:5000 <br>

### Flask Flexibility

- Flask provides developers generous flexibility for developing their web applications.<br>
- The official documentation is very thorough, providing lots of details with well-written examples.<br>
- Flask is arguably one of Python’s most popular web frameworks, with plenty of tutorials and libraries available to add to   your apps.<br>
- Flask is a lightweight framework with few dependencies. It takes just a few lines of Python to load Flask, and because it is    modular, you can restrict the dependencies to suit your needs.<br>
- Integration with database toolkits like SQLAlchemy, SQL databases like SQLite and MySQL, and NoSQL databases like    DynamoDB and MongoDB is relatively easy.<br>

## App

All server routes located within app directory- views.py

#### Endpoints

------------------------------------------------------------------------------------------------------------
| Method| Endpoint                 | Access Control | Description                                        |
| ------| -------------------------| ---------------| -------------------------------------------------- |
| GET   | `/index`                 | User           | Basic route to render `index.html` Home page       |
| GET   | `/register`              | User           | Renders `register.html` form for new registration. |
| POST  | `/register`              | User           | Accepts user credentials to register new user and update db User-table with hash-passwprd        |
| GET   | `/login`                 | User           | Renders `login.html` form for login                |
| POST  | `/login`                 | User           | User can login using his/her own credentials       |
| GET   | `/reset_password_request`| User           | Renders `reset_password_request.html` form for password reset request |
| POST  | `/reset_password/<token>`| User           |               |
| GET   | `/herokuapp`             | User           | Free as well as paid user can see stock-price sentimental analysis    |
| GET   | `/premium`               | User           | User can update as a premium user -pay and access data to decide right time to sell and buy              |
|       | `/pay`                   | User           | used `stripe` payment to accept the payment        |
|       | `/google_url`            | User           | User can login using his/her GOOGLE credentials    |
|       | `/github_url`            | User           | User can login using his/her GITHUB credentials    |
|       | `/twitter_url`           | User           | User can login using his/her TWITTER credentials   |
| GET   | `/contact`               | User           | renders `contact.html` form for contacting stock-price team  |
| POST  | `/contact`               | User           | accepts data from user and sends e-mail to stock-price mail-id |
------------------------------------------------------------------------------------------------------------

# Data Model

### App User Table

-------------------------------------------------------------------
| Name          | Data type     | Primary Key | Unique | Not NULL |
| ------------- |:-------------:|:-----------:|:------:|:--------:|
| id            | Interger      | +           | -      | -        |
| username      | String        | -           | +      | +        |
| email         | String        | -           | +      | +        |
| password_hash | String        | -           | -      | +        |
| premium_user  | Boolean       | -           | -      | -        |
-------------------------------------------------------------------

## Flask and Flask-extensions 

[Flask Documentation](http://flask.pocoo.org/docs/)
Flask is often referred to as a micro framework, because a core functionality includes WSGI and routing based on Werkzeug and template engine based on Jinja2. In addition, Flask framework has support for cookie and sessions as well as web helpers like JSON, static files etc. Obviously, this is not enough for the development of a full-fledged web application.
There are a large number of Flask extensions available. A Flask extension is a Python module, which adds specific type of support to the Flask application.

[Flask Extensions](http://flask.pocoo.org/extensions/)
These are the listed Flask-extensions used in this project
- `Flask-login` - Flask-Login provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users' sessions over extended periods of time.
- `Flask-migrate` - Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.
- `Flask-sqlchamy` - SQLAlchemy is the Python SQL toolkit and the Object Relational Mapper that gives application developers the full power and flexibility of SQL.
- `Flask-mail` - A web based application is often required to have a feature of sending mail to the users/clients. Flask-Mail extension makes it very easy to set up a simple interface with any email server.
- `Flask-dance` - Flask-Dance is an approved extension that allows developers to build Flask-based apps to allow users to authenticate via OAuth protocol.  
## Environment Variables

In order for the app to function correctly, the user must set up their own environment variables.

create a config.py(DON'T FORGET TO ADD IT TO `.gitignore`) file that includes the following:

### config.py
- import os
- basedir = os.path.abspath(os.path.dirname(__file__))
- class Config(object):
    - SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    - SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \ 'sqlite:///' + os.path.join(basedir, 'app.db')
    - SQLALCHEMY_TRACK_MODIFICATIONS = False
    - LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    - STRIPE_PUB_KEY `this is generated in the Stripe dashboard`
    - STRIPE_SECRET_KEY `this is generated in the Stripe dashboard`

    - GITHUB_CLIENT_ID  = `github developer key`
    - GITHUB_CLIENT_SECRET = `github developer key`

    - GOOGLE_CLIENT_ID = `google developer key`
    - GOOGLE_CLIENT_SECRET = `google developer key`

    - TWITTER_API_KEY = `twitter developer key`
    - TWITTER_API_SECRET  = `twitter developer key`

    - ADMINS = ['your-email@example.com']
    - MAIL_SERVER = `smtp.gmail.com`
    - MAIL_PORT =  587
    - MAIL_USE_TLS = True
    - MAIL_USERNAME = `'you@google.com`
    - MAIL_PASSWORD = `GooglePasswordHere`
    

See [Data Science](https://github.com/labs13-stock-price/data-science) for details on the fronend of our project.

