from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from app import app, db, models

from app.forms import FormLogin

from app.forms import FormInterfaceEdit, FormInterfaceAdd
from app.forms import FormHostTypeAdd, FormHostTypeEdit
from app.forms import FormHostAdd, FormHostEdit
from app.forms import FormCircuitAdd, FormCircuitEdit
from app.forms import FormVlan, FormVrf
from app.forms import FormIanaIfType



#from netaddr import IPNetwork
# http://pythonhosted.org//netaddr/tutorial_01.html

# None can be used for undefined columns in the database

#== backup plan
#from werkzeug.routing import Rule

#this stuff is a work around should a  multi-use error occur
# http://flask.pocoo.org/docs/patterns/viewdecorators/
#app.url_map.add(Rule('/', endpoint='index'))
#app.url_map.add(Rule('/index.html', endpoint='index'))
#app.endpoint('index')
#== end backup plan

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
  #http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates
  #Under the covers, the render_template function invokes the Jinja2 templating engine
  #  http://jinja.pocoo.org/
  #address = { 'dns': 'bm3-qvsl-vyat-00-001', 'ipv4': '199.63.45.56' }
  #return render_template( 'index.html', title="heading", address=address )
  return render_template( 'index.html' )

@app.route('/user/<name>')
@app.route('/user/<name>/')
def user(name):
  return '<h1>Hello, %s!</h1>' % name

## organization
# see viewOrganization.py

## ipaddress
# see viewIPAddress.py

## hosttype

@app.route('/hosttypes')
def hosttypes():
  return render_template( 'index.html' )

## host

@app.route('/hosts')
def hosts():
  return render_template( 'index.html' )

## circuit
@app.route('/circuits')
def circuits():
  return render_template( 'index.html' )

## interface

@app.route('/interfaces')
def interfaces():
  return render_template( 'index.html' )


#To handle web forms, use the Flask-WTF extension, 
#which in turn wraps the WTForms project in a way that integrates nicely with Flask apps.
#http://packages.python.org/Flask-WTF
#http://wtforms.simplecodes.com/docs/dev

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    ok = False
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        ok = True
        
    if (ok):
      return redirect('/index')
    else:
      return render_template('login.html', title = 'Sign In', form = form, providers = app.config['OPENID_PROVIDERS']) 

# http://flask.pocoo.org/docs/0.10/quickstart/#redirects-and-errors
@app.errorhandler(404)
def ErrorNotFound( error ):
  return render_template( 'error.html' ), 404



# http://stackoverflow.com/questions/12505158/generating-a-uuid-in-postgres-for-insert-statement
# select uuid_in((md5(random()||now()::text))::cstring);
