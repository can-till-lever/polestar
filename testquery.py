import os
import re
import datetime

import uuid
import ipaddress

import pdb

from app import app, db, models
from sqlalchemy.dialects import postgresql
from sqlalchemy import and_

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object( 'config' )
db = SQLAlchemy(app)

from app.models import TableIpAddress

def test():

  ip = ipaddress.IPv4Network('10.21.0.12/30')
#  ip = ipaddress.network_address('10.12.0.12/30')
  #ip = '10.12.0.12'

  #if 0 == models.TableIpAddress.query.filter(and_(str(TableIpAddress.ipaddress) == ip, TableIpAddress.fqdn == fqdn ) ).count():
  #  print( fqdn, ': not found')
  #else:
  #  print( fqdn, ': no insertion, already exists' )
  
#  pdb.set_trace()
  if 0 == models.TableIpAddress.query.filter( TableIpAddress.ipaddress == ip ).count():
    print( ip, ': not found')
  else:
    print( ip, ': no insertion, already exists' )

  #if 0 == models.TableIpAddress.query.filter(TableIpAddress.fqdn == fqdn ).count():
  #  print( fqdn, ': not found')
  #else:
  #  print( fqdn, ': found' )
   
   
if __name__ == '__main__':
  test()
