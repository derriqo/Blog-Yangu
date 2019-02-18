from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required
from ..models import User
from .forms import UpdateProfile
from urllib import request
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