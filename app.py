"""Blogly application."""

from flask import Flask, request, redirect, render_template
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    """redirects to list of users"""

    return render_template('posts.html', posts = posts)

@app.route('/users')
def list_users():
    """shows all users"""

    users = User.query.all()
    return render_template('user_list.html', users = users)

@app.route('/users/new')
def render_user_form():
    """renders new user form"""

    return render_template('add_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """posts user form data to create new user"""

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
    user_posts = Post.query.filter_by(user_id = user_id).all()
    return render_template('user_details.html', user = user, posts = user_posts)

@app.route('/users/<int:user_id>/edit')
def render_edit_user(user_id):
    """renders data form to edit user information"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def post_edit_post(user_id):
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

@app.route('/users/<int:user_id>/posts/new')
def render_add_post_form(user_id):
    """shows the add post form to the user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('add_post.html', user=user, tags = tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_new_post(user_id):
    """creates user new post"""

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('post_tag')
    new_post_tags = Tag.query.filter(Tag.id.in_(tags)).all()

   
    new_post = Post(title=title, content=content, user_id=user_id, tags = new_post_tags)

    db.session.add(new_post)
    db.session.commit()

    # for tag in tags:
   
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """show post detail"""

    post = Post.query.get_or_404(post_id)
    user = post.users
    tags = post.tags

    return render_template('post_details.html', post = post, user = user, tags = tags)

@app.route('/posts/<int:post_id>/edit')
def render_edit_post_form(post_id):
    """shows form to edit post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    user = post.users

    return render_template('edit_post.html', post = post, user = user, tags = tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_post_edit(post_id):
    """renders data form to edit user information"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tags = request.form.getlist('post_tag')
    post.tags = Tag.query.filter(Tag.id.in_(tags)).all()

    db.session.add(post)
    db.session.commit()
 
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    user = post.users 

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/tags')
def show_tags_list():

    tags = Tag.query.all()

    return render_template('tag_list.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('tag_details.html', tag = tag, posts = posts)

@app.route('/tags/new')
def render_add_tag_form():

    return render_template('add_tag.html')

@app.route('/tags/new', methods=["POST"])
def create_tag():

    name = request.form['name']
    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def render_edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    

    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def post_tag_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tag_name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')







