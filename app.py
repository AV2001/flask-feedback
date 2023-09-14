from flask import Flask, flash, redirect, render_template
from models import db, User
from forms import RegisterForm, LoginForm

# Create instance of Flask.
app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'flask_feedback_admin'

# Register the database.
db.init_app(app)


@app.route('/')
def home_page():
    '''Redirect to register form.'''
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    '''Register'''
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/secret')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    '''Login'''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            flash('Login Successful!', 'success')
            return redirect('/secret')
        else:
            form.username.errors.append('Invalid username/password!')
    return render_template('login.html', form=form)


@app.route('/secret')
def show_secret():
    return '<h1>You made it!</h1>'
