from flask import render_template
from . import main
from flask_login import login_required

#Views 
@main.route('/',methods = ['GET','POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''

    return render_template('index.html')