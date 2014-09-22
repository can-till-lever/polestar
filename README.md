<h1>NodeStar</h1>

Test using Python to build an Infrastructure Management Application.  Requires Python 3.3 or greater.

Development suspended due to some troubleshooting issues with py-postgresql library in sqlalchemy.  Basic issue
appears to be that py-postgresql has some issues with cidr style field types.  I could go with psycopg2, but 
havn't bitten that bullet yet.

<br>sudo apt-get install build-essential
<br>sudo apt-get install python3-dev

<br>mkdir polestar
<br>cd polestar

<br>virtualenv --python=/usr/bin/python3 env
<br>. env/bin/activate

<br>mkdir app
<br>mkdir app/static
<br>mkdir app/templates
<br>mkdir tmp

<br>pip install flask
<br>pip install flask-login
<br>pip install flask-openid
<br>pip install flask-mail
<br>pip install sqlalchemy
<br>pip install flask-sqlalchemy
<br>pip install sqlalchemy-migrate
<br>pip install flask-migrate
<br>pip install flask-whooshalchemy
<br>pip install flask-wtf
<br>pip install pytz
<br>pip install flask-babel
<br>pip install flup
<br>pip install py-postgresql
<br>pip install netaddr

<br>sudo su - postgres
<br>psql
<br>create role polestar login password 'starring';
<br>create database polestar with owner polestar;

<br>from app import db
<br>db_create_all()
