import os
import re
import xml.etree.ElementTree as ET
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

tree = ET.parse( 'import/exported_data.xml' )
root = tree.getroot()

#for child in root:
#  print( '/%s/  |%s|' % (child.tag, child.attrib) )

# look for network: comment, ipv4_network, name
# look for host: name, comment sub mvia_address
# look for router:  (multiple), logical_interface?, 
# look for physical_interface: comment, macaddress, sub vlan_interface: interface_id
# look for firewall_node, sub mvia_address

for element in root.iter('network'):
  #print(element.attrib)
  attrib = element.attrib
  #print( attrib['name'], attrib['ipv4_network'], attrib['comment'] if 'comment' in attrib else '' )
  addr = TableIpAddress()
  addr.idorganization = 'QVSL'
  addr.idipaddress = uuid.uuid4()
  addr.ipaddress = attrib['ipv4_network']
  addr.name = attrib['name'].lower()
  if 'comment' in attrib:
    addr.description = attrib['comment']
  addr.source = 'importsmc network'
  addr.datetimecreation = datetime.datetime.now()
  db.session.add( addr)
  db.session.commit()
  
  
for element in root.iter('host'):
  #print(element.attrib)
  attrib1 = element.attrib
  #print( '==', attrib['name'], attrib['comment'] if 'comment' in attrib else '' )
  for sub in element.iter('mvia_address'): # has other stuff in addition to this
    #print( sub.attrib['address'] if 'address' in sub.attrib else '' )
    attrib2 = sub.attrib
    if 'address' in attrib2:
      addr = TableIpAddress()
      addr.idorganization = 'QVSL'
      addr.idipaddress = uuid.uuid4()
      #addr.ipaddress = attrib['ipv4_network']
      addr.name = attrib1['name'].lower()
      if 'comment' in attrib:
        addr.description = attrib1['comment']
      addr.ipaddress = attrib2['address'] 
      addr.source = 'importsmc host'
      #addr.datetimecreation = str(datetime.datetime.now().isoformat())
      addr.datetimecreation = datetime.datetime.now()
      db.session.add( addr)
      db.session.commit()
    
    
    