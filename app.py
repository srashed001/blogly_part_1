"""Blogly application."""

from flask import Flask, request, redirect, render_template
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'abc123'

# toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_list():
    """redirects to list of users"""

    return redirect('/users')


@app.route('/users')
def list_users():
    """shows all users"""

    users = User.query.all()
    return render_template('list.html', users = users)

@app.route('/users/new')
def add_user_form():
    """renders new user form"""

    return render_template('add_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """user form data to create new user"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """shows user details page based on user_id param"""

    user = User.query.get_or_404(user_id)
    return render_template('details.html', user = user)

@app.route('/users/<int:user_id>/edit')
def render_edit_user(user_id):
    """renders data form to edit user information"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_data.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def post_edit_user(user_id):
    """renders data form to edit user information"""

    user = User.query.get_or_404(user_id)
    
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """deletes user from database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

