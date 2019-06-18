import os
basedir = os.path.abspath(os.path.dirname(__file__))
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    STRIPE_PUB_KEY = 'pk_test_lGXe3xx2KfcxVMohkNhLQLzn00f0OXjTw8'
    STRIPE_SECRET_KEY = 'sk_test_lKL5mpbIp5XQh3X750dAA8yr00laScgXRm'

    GITHUB_CLIENT_ID = '791581e9ffc8f28c4ca5'
    GITHUB_CLIENT_SECRET = '416371fc9da3849a8108279e4d2f0ec23f8bf816'

    GOOGLE_CLIENT_ID = '903410342783-tkq7ou8hcj2imb6vnbsd3qujmo2up5o2.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '8QY_uP1Jc6aAmgin4T1gaFsD'

    TWITTER_ = ''
    TWITTER_ = ''

    #password RESET
    ADMINS = ['for.stock.price.app@gmail.com']
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'for.stock.price.app@gmail.com'
    MAIL_PASSWORD = 'Test12345#'
