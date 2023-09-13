from flask import Flask, redirect, render_template
from models import db, User
from forms import RegisterForm

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
def show_register_form():
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
