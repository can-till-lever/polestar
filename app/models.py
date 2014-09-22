from app import db
from sqlalchemy.dialects import postgresql

#part of schema definition
#boolean:  primary_key, unique, index, nullable
#value:  default
# db. Integer, String(size), Text, DateTime, Float, Boolean, PIckleType, LargeBinary

# http://python.projects.pgfoundry.org/

# docs.sqlalchemy.org/en/latest/core/metadata.html

class TableBase(db.Model):  # a base class, not used anywhere yet, but provides an example of declaration
  __abstract__ = True
  id = db.Column( db.Integer, primary_key=True)

class TableOrganization(db.Model):
  __tablename__ = 'organization'
  idorganization = db.Column( db.Text, primary_key=True )
  name = db.Column( db.Text, index = True, nullable = False )
  description = db.Column( db.Text, default = '' )
  asn = db.Column( db.Integer )
  url = db.Column( db.Text, default = '' )
  ipaddresses = db.relationship( 'TableIpAddress', backref='organization', lazy='dynamic' )

# ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
# a class, as defined using the Declarative system, has been provided with a constructor (e.g. __init__() method) which automatically accepts keyword names that match the columns we’ve mapped.
# we are free to define any explicit __init__() method we prefer on our class, which will override the default method provided by Declarative.

#  def __init__(self, idorganization, name ):
#    self.id = idorganization
#    self.name = name
  
  def __repr__(self):
    return 'Organization: %s - %s' % (self.idorganization, self.name)

class TableIanaiftype(db.Model):
  __tablename__ = 'ianaiftype'
  idianaiftype = db.Column( db.Integer, primary_key=True )
  name = db.Column( db.Text, nullable=False )
  description = db.Column( db.Text, default='' )
  
  def __repr__(self):
    return '<ianaiftype %r>' % (self.name)
  
class TableVlan(db.Model):
  __tablename__ = 'vlan'
  idvlan = db.Column( postgresql.UUID, primary_key=True )
  vlan = db.Column( db.Integer ) 
  description = db.Column( db.Text, default='' )
  
  def __repr__(self):
    return '<vlan %r>' % (self.vlan)
  
class TableVrf(db.Model):
  __tablename__ = 'vrf'
  idvrf = db.Column( postgresql.UUID, primary_key=True )
  vrf = db.Column( db.Text )
  description = db.Column( db.Text, default='' )
  
  def __repr__(self):
    return '<vrf %r>' % (self.vrf)
  
class TableIpAddress(db.Model):
  __tablename__ = 'ipaddress'
  idipaddress = db.Column( postgresql.UUID, primary_key=True )
  parent = db.Column( postgresql.UUID, db.ForeignKey( 'ipaddress.idipaddress'), nullable=True )
#  ipaddress = db.Column( postgresql.INET, index=True, nullable=False ) # driver doesn't do the /xx aspect, even though postgresql does
  ipaddress = db.Column( postgresql.CIDR, index=True, nullable=False )  # driver alloes the /xx aspect, 
  idorganization = db.Column( db.Text, db.ForeignKey( 'organization.idorganization'), nullable=False )
  name = db.Column( db.Text, nullable=False )
  description = db.Column( db.Text, default='' )
  fqdn = db.Column( db.Text, default='' )
  url = db.Column( db.Text, default='' )
  source = db.Column( db.Text, default='' ) # software module used for creating the entry
  datetimecreation = db.Column( postgresql.TIMESTAMP, nullable=False )
  
  def __repr__(self):
    return '<ipaddress %r>' % (self.name)
  
class TableCircuit(db.Model):
  __tablename__ = 'circuit'
  idcircuit = db.Column( postgresql.UUID, primary_key=True )
  parent = db.Column( postgresql.UUID, db.ForeignKey( 'circuit.idcircuit'), nullable=True )
  name = db.Column( db.Text, nullable=False )
  idipaddress = db.Column( postgresql.UUID, db.ForeignKey( 'ipaddress.idipaddress'), nullable=True )
  description = db.Column( db.Text, default='' )
  url = db.Column( db.Text, default='' )
#  interfaces = db.relationship( 'interface', backref='idcircuit', lazy='dynamic' )
  
  def __repr__(self):
    return '<circuit %r>' % (self.name)
  
class TableHostType(db.Model):
  __tablename__ = 'hosttype'
  idhosttype = db.Column( postgresql.UUID, primary_key=True )
  name = db.Column( db.Text, nullable=False )
  description = db.Column( db.Text, default='' )
 # hosts = db.relationship( 'host', backref='idhosttype', lazy='dynamic' )
  
  def __repr__(self):
    return '<hosttype %r>' % (self.idhosttype)
  
class TableHost(db.Model):
  __tablename__ = 'host'
  idhost = db.Column( postgresql.UUID, primary_key=True )
  parent = db.Column( postgresql.UUID, db.ForeignKey( 'host.idhost' ), nullable=True )
  name = db.Column( db.Text, nullable=False )
  idhosttype = db.Column( postgresql.UUID, db.ForeignKey( 'hosttype.idhosttype' ), nullable=False )
  description = db.Column( db.Text, default='' )
  url1 = db.Column( db.Text, default='' )
  url2 = db.Column( db.Text, default='' )
#  interfaces = db.relationship( 'interface', backref = 'idhost', lazy='dynamic' )
  
  def __repr__(self):
    return '<host %r>' % (self.idhost)
  
class TableInterface(db.Model):
  __tablename__ = 'interface'
  idinterface = db.Column( postgresql.UUID, primary_key=True )
  parent = db.Column( postgresql.UUID, db.ForeignKey( 'interface.idinterface' ),  nullable=True )
  idhost = db.Column( postgresql.UUID, db.ForeignKey( 'host.idhost' ), nullable=False )
  idipaddress = db.Column( postgresql.UUID, db.ForeignKey( 'ipaddress.idipaddress' ), nullable=True )
  name = db.Column( db.Text, nullable=False )
  macaddress = db.Column( postgresql.MACADDR )
  description = db.Column( db.Text, default='' )
  fqdn = db.Column( db.Text, default='' )
  url = db.Column( db.Text, default='' )
  idianaiftype = db.Column( db.Integer, db.ForeignKey( 'ianaiftype.idianaiftype' ), nullable=True )  # change to false ultimately
  idvlan = db.Column( postgresql.UUID, db.ForeignKey( 'vlan.idvlan' ), nullable=True )
  idvrf = db.Column( postgresql.UUID, db.ForeignKey( 'vrf.idvrf' ), nullable=True )
  idcircuit = db.Column( postgresql.UUID, db.ForeignKey( 'circuit.idcircuit' ), nullable=True )
  
    
  def __repr__(self):
    return '<interface %r>' % (self.idinterface)

