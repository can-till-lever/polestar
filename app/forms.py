#from flask.ext.wtf import Form
import uuid

from netaddr import IPNetwork, AddrFormatError

from flask_wtf import Form
from wtforms import TextField, BooleanField, IntegerField, HiddenField, SelectField
from wtforms.validators import Optional, Required, Length, IPAddress, URL, UUID, MacAddress
from wtforms import ValidationError

# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# http://wtforms.readthedocs.org/en/latest/validators.html

class FormLogin(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)



class FormOrganizationEdit( Form ):
  name = TextField('name', validators = [Required()])
  description = TextField('description', validators = [Length( min=0, max=100)])
  asn = IntegerField( 'asn', validators = [Optional()], description="BGP ASN" )
  url = TextField( 'url', validators = [Optional(), URL()] )

class FormOrganizationAdd( FormOrganizationEdit ):
  idorganization = TextField( 'idorganization', 
                              validators = [ Required(), Length( min=4, max=4, message = 'Field must be 4 characters long.' )])

# http://wtforms.readthedocs.org/en/latest/validators.html
class ValidateIpAddress(object):
  def __init__(self, message=None):
    if not message:
      message = u'Badly formed CIDR'
    self.message = message
    
  def __call__(self, form, field):
    try:
      IPNetwork(field.data)
    except AddrFormatError:
      raise ValidationError(self.message)

class FormIpAddressAdd( Form ):
#  ipaddress = TextField( 'ipaddress', validators = [Required(), IPAddress(ipv4=True, ipv6=True) ]) # doesn't allow cidr formats
  ipaddress = TextField( 'ipaddress', validators = [Required(), ValidateIpAddress()] )
  parent = SelectField( 'parent', validators = [Optional(), UUID() ], coerce=str ) # show the enclosing ip address rather than the key
  idorganization = SelectField( 'idorganization', validators = [Required()] )
  name = TextField( 'name' ) # optional name
  description = TextField( 'description' ) # optional description
  fqdn = TextField( 'fqdn', validators = [Optional()] )
  url = TextField( 'url' ) # optional url for management or for info

class FormIpAddressEdit( FormIpAddressAdd ):
  idipaddress = HiddenField( 'idipaddress', validators = [Required()])

class FormIanaIfType( Form ):
  idianaiftype = HiddenField( 'idianaiftype', validators = [ Required() ] )
  name = TextField( 'name', validators = [Required()] )
  description = TextField( 'description' )

class FormInterfaceAdd( Form ):
  parent = SelectField( 'parent' )
  idhost = SelectField( 'idhost', validators = [Required()] )
  idipaddress = SelectField( 'idipaddress' )
  idcircuit = SelectField( 'idcircuit' )
  name = TextField( 'name' )
  mac = TextField( 'mac' )
  description = TextField( 'description' )
  fqdn = TextField( 'fqdn' )
  url = TextField( 'url' )
  idvlan = HiddenField( 'idvlan' )
  idvrf = HiddenField( 'idvrf' )

class FormInterfaceEdit( FormInterfaceAdd ):
  idinterface = HiddenField( 'idinterface', validators = [Required()] )

class FormCircuitAdd( Form ):
  parent = SelectField( 'parent' )
  name = TextField( 'name', validators = [Required()] )
  idipaddress = SelectField( 'idipaddress' )
  description = TextField( 'description' )
  url = TextField( 'url' )

class FormCircuitEdit( FormCircuitAdd ):
  idcircuit = HiddenField( 'idcircuit', validators = [Required()] )

class FormHostTypeAdd( Form ):
  name = TextField( 'name', validators = [Required()] )
  description = TextField( 'description' )

class FormHostTypeEdit( FormHostTypeAdd ):
  idhosttype = HiddenField( 'idhosttype', validators = [Required() ] )

class FormHostAdd( Form ):
  parent = SelectField( 'parent' )
  name = TextField( 'name', validators = [Required()] )
  idhosttype = SelectField( 'idhosttype', validators = [ Required() ] )
  description = TextField( 'description' )
  url1 = TextField( 'url1' )
  url2 = TextField( 'url2' )

class FormHostEdit( FormHostAdd ):
  idhost = HiddenField( 'idhost', validators = [Required()] )

class FormVlan( Form ):
  idvlan = HiddenField( 'idvlan', validators = [Required()] )
  vlan = TextField( 'vlan', validators = [ Required() ] )
  name = TextField( 'name', validators = [ Required() ] )
  description = TextField( 'description' )

class FormVrf( Form ):
  idvrf = HiddenField( 'idvrf', validators = [Required()] )
  vrf = TextField( 'vrf', validators = [ Required() ] )
  description = TextField( 'description' )
    