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

## Migrations

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

🚫This is just an example. Replace this with your data model

#### 2️⃣ ORGANIZATIONS

---

```
{
  id: UUID
  name: STRING
  industry: STRING
  paid: BOOLEAN
  customer_id: STRING
  subscription_id: STRING
}
```

#### USERS

---

```
{
  id: UUID
  organization_id: UUID foreign key in ORGANIZATIONS table
  first_name: STRING
  last_name: STRING
  role: STRING [ 'owner', 'supervisor', 'employee' ]
  email: STRING
  phone: STRING
  cal_visit: BOOLEAN
  emp_visit: BOOLEAN
  emailpref: BOOLEAN
  phonepref: BOOLEAN
}
```

## 2️⃣ Actions

🚫 This is an example, replace this with the actions that pertain to your backend

`getOrgs()` -> Returns all organizations

`getOrg(orgId)` -> Returns a single organization by ID

`addOrg(org)` -> Returns the created org

`updateOrg(orgId)` -> Update an organization by ID

`deleteOrg(orgId)` -> Delete an organization by ID
<br>
<br>
<br>
`getUsers(orgId)` -> if no param all users

`getUser(userId)` -> Returns a single user by user ID

`addUser(user object)` --> Creates a new user and returns that user. Also creates 7 availabilities defaulted to hours of operation for their organization.

`updateUser(userId, changes object)` -> Updates a single user by ID.

`deleteUser(userId)` -> deletes everything dependent on the user

## 3️⃣ Environment Variables

In order for the app to function correctly, the user must set up their own environment variables.

create a .env file that includes the following:

🚫 These are just examples, replace them with the specifics for your app
    
    *  STAGING_DB - optional development db for using functionality not available in SQLite
    *  NODE_ENV - set to "development" until ready for "production"
    *  JWT_SECRET - you can generate this by using a python shell and running import random''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#\$%^&amp;*(-*=+)') for i in range(50)])
    *  SENDGRID_API_KEY - this is generated in your Sendgrid account
    *  stripe_secret - this is generated in the Stripe dashboard
    
## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./code_of_conduct.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

## Documentation

See [Frontend Documentation](🚫link to your frontend readme here) for details on the fronend of our project.
🚫 Add DS iOS and/or Andriod links here if applicable.


Test
