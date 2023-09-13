from flask import Flask, render_template
from models import db, User

# Create instance of Flask.
app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register the database.
db.init_app(app)


@app.route('/')
def home_page():
    '''Show the home page.'''
    return render_template('index.html')
