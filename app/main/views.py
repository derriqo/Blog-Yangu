from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required
from ..models import User,Blog
from .forms import UpdateProfile,BlogForm
from urllib import request
from .. import db, photos
import json
import threading

#Views 
@main.route('/')
@login_required
def index():

    '''
    View root page function that returns the index page and its data

    '''
    response = request.urlopen('http://quotes.stormconsultancy.co.uk/random.json')

    if response.code==200:
      read_Data=response.read()

      JSON_object = json.loads(read_Data.decode('UTF-8'))
      print(JSON_object)
      author = JSON_object['author']
      id = JSON_object['id']
      quote = JSON_object['quote']
      permalink = JSON_object['permalink']

      head = "Welcome to my Blog"
      # return render_template('index.html',head=head)
      return render_template("index.html", head = head, author = author, id = id, quote = quote, permalink = permalink)

    return render_template('index.html')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/blog/new',methods = ['GET','POST'])
@login_required
def new_blog():

    form =BlogForm()

    if form.validate_on_submit():
        blog = Blog(title=form.title.data, content=form.content.data, user_id=current_user)
        db.session.add(blog)
        db.session.commit()
        flash('Your blog is ready!','success')
        
        return redirect(url_for('blog.html'))

    return render_template('create_blog.html',title = 'New Blog',form =form, legend='New Blog')


@main.route("/blogs")
def blog():
    blog = Blog.query.order_by(Blog.date_posted.desc())
    return render_template('blog.html', blog=blog)


@main.route("/blog/<int:blog_id>/update", methods=['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.author != current_user:
        abort(403)
    form = BlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        flash('Your blog has been updated!', 'success')
        return redirect(url_for('blog', blog_id=blog.id))
    elif request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content
    return render_template('create_blog.html', title='Update Blog',form=form, legend='Update Blog')


@main.route("/blog/<int:blog_id>/delete", methods=['Blog'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.author != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
    flash('Your blog has been deleted!', 'success')
    return redirect(url_for('home'))
