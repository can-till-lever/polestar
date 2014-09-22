import os
import re
import datetime

import uuid

from app import app, db, models
from sqlalchemy.dialects import postgresql
from sqlalchemy import and_

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object( 'config' )
db = SQLAlchemy(app)

from app.models import TableIpAddress

def SaveBlock( org, name, ip, description, url = '' ):
  addr = TableIpAddress()
  addr.idipaddress = uuid.uuid4()
  addr.ipaddress = ip
  #addr.fqdn = fqdn
  addr.name = name
  addr.description = description
  addr.idorganization = org
  addr.url = url
  addr.source = 'populateipblocks'
  addr.datetimecreation = datetime.datetime.now()
  db.session.add( addr )
  db.session.commit()

def SaveBlocks( org ):
  # http://en.wikipedia.org/wiki/List_of_assigned_/8_IPv4_address_blocks
  # http://en.wikipedia.org/wiki/Reserved_IP_addresses
  SaveBlock( org, 'IANA', '0.0.0.0/8', 'reserved' )
  SaveBlock( org, 'IANA Private', '10.0.0.0/8', 'RFC1918', 'http://tools.ietf.org/html/rfc1918' )
  SaveBlock( org, 'IANA', '100.64.0.0/10', 'RFC6598 Carrier Grade NAT', 'http://tools.ietf.org/html/rfc6598')
  SaveBlock( org, 'IANA Loopback', '127.0.0.0/8', 'loopback' )
  SaveBlock( org, 'IANA', '169.254.0.0/16', 'RFC3927 autoconfiguration', 'http://tools.ietf.org/html/rfc3927' )
  SaveBlock( org, 'ARIN', '172.0.0.0/8', 'various' )
  SaveBlock( org, 'ARIN private', '172.16.0.0/12', 'RFC1918', 'http://tools.ietf.org/html/rfc1918' )
  SaveBlock( org, 'ARIN', '192.0.0.0/8', 'various' )
  SaveBlock( org, 'IANA', '192.0.2.0/24', 'RFC5737 TEST-NET-1', 'http://tools.ietf.org/html/rfc5737' )
  SaveBlock( org, 'ARIN private', '192.168.0.0/16', 'RFC1918', 'http://tools.ietf.org/html/rfc1918' )
  SaveBlock( org, 'ARIN', '192.0.0.0/24', 'RFC5736', 'http://tools.ietf.org/html/rfc5736' )
  SaveBlock( org, 'ARIN', '198.0.0.0/8', 'various' )
  SaveBlock( org, 'ARIN', '198.18.0.0/15', 'RFC5735', 'http://tools.ietf.org/html/rfc5735' )
  SaveBlock( org, 'ARIN', '198.51.100.0/24', 'RFC5735 TEST-NET-2', 'http://tools.ietf.org/html/rfc5735' )
  SaveBlock( org, 'APNIC', '203.0.0.0/8', 'various')
  SaveBlock( org, 'APNIC', '203.0.113.0/24', 'RFC5737 TEST-NET-3', 'http://tools.ietf.org/html/rfc5737' )
  SaveBlock( org, 'Multicast', '224.0.0.0/4', 'RFC5771', 'http://tools.ietf.org/html/rfc5771' )
  SaveBlock( org, 'Future Use', '240.0.0.0/4', 'RFC1112', 'http://tools.ietf.org/html/rfc1112')
  
SaveBlocks( 'QVSL')  
