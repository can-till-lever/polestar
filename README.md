<h1>NodeStar</h1>

Test using Python to build an Infrastructure Management Application.  Requires Python 3.3 or greater.

Development suspended due to some troubleshooting issues with py-postgresql library in sqlalchemy.  Basic issue
appears to be that py-postgresql has some issues with cidr style field types.  I could go with psycopg2, but 
havn't bitten that bullet yet.

sudo apt-get install build-essential
sudo apt-get install python3-dev

mkdir polestar
cd polestar

virtualenv --python=/usr/bin/python3 env
. env/bin/activate

mkdir app
mkdir app/static
mkdir app/templates
mkdir tmp

pip install flask
pip install flask-login
pip install flask-openid
pip install flask-mail
pip install sqlalchemy
pip install flask-sqlalchemy
pip install sqlalchemy-migrate
pip install flask-migrate
pip install flask-whooshalchemy
pip install flask-wtf
pip install pytz
pip install flask-babel
#pip install flup
pip install py-postgresql
pip install netaddr

sudo su - postgres
psql
create role polestar login password 'starring';
create database polestar with owner polestar;

>>>from app import db
>>>db_create_all()
