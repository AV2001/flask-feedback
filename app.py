from flask import Flask, flash, redirect, render_template, request, session
from models import db, User, Feedback
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
        logged_in_user = User.query.get(username)
        if logged_in_user.username == session['username']:
            return render_template('user-profile.html', user=logged_in_user)
        else:
            return redirect(f'/users/{session["username"]}')
    else:
        flash('Cannot access resource unless logged in!', 'danger')
        return redirect('/login')


@app.route('/logout')
def logout():
    '''Logout'''
    session.pop('username')
    flash('You are logged out!', 'info')
    return redirect('/')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    '''Delete a particular user.'''
    user = User.query.get(username)
    # Only delete the user if they are logged in
    if 'username' in session and user.username == session['username']:
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash('Account deleted successfully!', 'success')
        return redirect('/')
    flash('Please login to delete your account!', 'danger')
    return redirect('/login')


@app.route('/users/<username>/feedback/add')
def show_add_feedback_form(username):
    '''Show feedback form for the logged in user.'''
    if 'username' in session:
        logged_in_user = User.query.get(username)
        if logged_in_user.username == session['username']:
            return render_template('add-feedback-form.html')
        else:
            return redirect(f'/users/{session["username"]}')
    else:
        flash('You must be logged in!', 'danger')
        return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['POST'])
def add_feedback(username):
    '''Process form to add feedback.'''
    title = request.form['title']
    content = request.form['content']
    user = User.query.get(username)
    new_feedback = Feedback(
        title=title, content=content, username=user.username)
    if 'username' in session:
        logged_in_user = User.query.get(username)
        if logged_in_user.username == session['username']:
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
    else:
        flash('You must be logged in!', 'danger')
        return redirect('/')


@app.route('/feedback/<int:id>/update')
def show_update_feedback_form(id):
    '''Show the update feedback form.'''
    if 'username' in session:
        feedback = Feedback.query.get(id)
        if session['username'] == feedback.username:
            return render_template('update-feedback-form.html', feedback=feedback)
        else:
            return redirect(f'/users/{session["username"]}')
    else:
        flash('You must be logged in!', 'danger')
        return redirect('/')
