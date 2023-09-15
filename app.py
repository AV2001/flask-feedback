from flask import Flask, flash, redirect, render_template, session
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
        new_user = User.register(
            username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        flash('Account Created Successfully!', 'success')
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    '''Login'''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash('Login Successful!', 'success')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors.append('Invalid username/password!')
    return render_template('login.html', form=form)


@app.route('/users/<username>')
def get_user(username):
    '''Show profile information about a user.'''
    if 'username' in session:
        user = User.query.get(username)
        return render_template('user-profile.html', user=user)
    else:
        flash('Cannot access resource unless logged in!', 'danger')
        return redirect('/login')


@app.route('/logout')
def logout():
    '''Logout'''
    session.pop('username')
    flash('You are logged out!', 'info')
    return redirect('/')
