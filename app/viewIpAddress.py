import uuid

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from app import app, db, models

from app.forms import FormIpAddressEdit, FormIpAddressAdd

from app.models import TableIpAddress, TableOrganization

from sqlalchemy.dialects import postgresql

@app.route('/ipaddresses')
def ipaddresses():
#  selection = list(r.db('qv').table('ipaddress').run( g.rdb_conn ))
  #selection = r.db('qv').table('ipaddress').order_by('ipaddress').run( g.rdb_conn )
  selection = models.TableIpAddress.query.all()
  final = []
  for record in selection:
    newrec = {}
    newrec['idipaddress'] = record.idipaddress
    newrec['ipaddress'] = record.ipaddress
    newrec['idorganization'] = record.idorganization
    newrec['name'] = record.name
    newrec['description'] = record.description
    newrec['fqdn'] = record.fqdn
    newrec['url'] = record.url
    
    if None != record.parent:
      #selectParent = r.db('qv').table('ipaddress').get(record['parent']).run(g.rdb_conn)
      selectParent = models.TableIpAddress.query.get(record.parent)
      newrec['parent'] = selectParent.ipaddress
    final.append(newrec)
  return render_template( 'ipaddress.html', ipaddresses=final )
#  return render_template( 'ipaddress.html', ipaddresses=selection )

def ipaddress_loadformchoices( form, exclusion ):
  
  #selectOrganization = r.db('qv').table('organization').run(g.rdb_conn)
  selectOrganization = models.TableOrganization.query.order_by(TableOrganization.idorganization).all()
  form.idorganization.choices = [ (item.idorganization, item.name) for item in selectOrganization ]

  #selectParent = r.db('qv').table('ipaddress').run(g.rdb_conn)
  selectParent = models.TableIpAddress.query.all()       
  form.parent.choices  = [( '', 'no parent' )]
  for item in selectParent:
    if str(item.idipaddress) in exclusion:
      pass
    else:
#      form.parent.choices += [(str(item.idipaddress),item.ipaddress) for item in selectParent ]  # don't create a circular link
      form.parent.choices += [(str(item.idipaddress),item.ipaddress)]  # don't create a circular link

def ipaddress_assign( form, table ):
  
  if 0 != len(form.parent.data):
    table.parent = form.parent.data
  else:
    pass #should assign null
  table.ipaddress = form.ipaddress.data
  #table.ipaddress = '10.0.0.0/8'
  table.idorganization = form.idorganization.data
  table.name = form.name.data
  table.description = form.description.data
  table.fqdn = form.fqdn.data
  table.url = form.url.data

@app.route('/ipaddress/add', methods=['GET'])
def ipaddress_add_get():

  form = FormIpAddressAdd()

  ipaddress_loadformchoices( form, [] )

  form.idorganization.data = 'QVSL'
  return render_template( 'ipaddress_edit.html', form=form, mode='add' )

@app.route('/ipaddress/add', methods=['POST'])
def ipaddress_add_post():

  form = FormIpAddressAdd()

  ipaddress_loadformchoices( form, [] )     # seems to need this for the validator

  if form.validate_on_submit():
    # need to check for redundant ipaddress for the specific idorganization
    addr = TableIpAddress()
    ipaddress_assign( form, addr )
    addr.idipaddress = uuid.uuid4()
    db.session.add( addr )
    db.session.commit()
    flash('ip address added')
    return redirect( url_for( 'ipaddresses' ) )
  else:
    # errors will be reported in the page via form messages
    return render_template( 'ipaddress_edit.html', form=form, mode='add' )

@app.route('/ipaddress/edit/<idipaddress>', methods=['GET'] )
def ipaddress_edit_get( idipaddress ):

  form = FormIpAddressEdit()
  
  ipaddress_loadformchoices( form, [idipaddress] )

  selection = models.TableIpAddress.query.get(idipaddress)  # need to error check this

  form.idipaddress.data = selection.idipaddress
  form.ipaddress.data = selection.ipaddress
  form.idorganization.data = selection.idorganization
  if None == selection.parent:
    form.parent.data = ''
  else:
    form.parent.data = str(selection.parent)
  form.name.data = selection.name
  form.description.data = selection.description
  form.fqdn.data = selection.fqdn
  form.url.data = selection.url
  
  return render_template( 'ipaddress_edit.html', form=form, mode='edit' )

@app.route('/ipaddress/edit/<idipaddress>', methods=['POST'] )
def ipaddress_edit_post( idipaddress ):

  form = FormIpAddressEdit()
  
  ipaddress_loadformchoices( form, [idipaddress] )
  
  print( form.parent.data )
  
  #if form.validate_on_submit():
  if form.is_submitted():
    if form.validate():
      #r.db('qv').table('ipaddress').get(idipaddress).update(form.data).run(g.rdb_conn)
      addr = models.TableIpAddress.query.get(idipaddress)  # validate proper record
      ipaddress_assign( form, addr )
      db.session.add( addr )
      db.session.commit()
      flash('ipaddress changes saved')
      return redirect( url_for( 'ipaddresses' ) )
    else:
      # errors will be reported in the page via form messages
      return render_template( 'ipaddress_edit.html',form=form, mode='edit' )

@app.route('/ipaddress/delete/<idipaddress>', methods=['GET'])
def ipaddress_delete( idipaddress ):
#  if      0 == r.db('qv').table('circuit').filter({'idipaddress':idipaddress}).count().run(g.rdb_conn) \
#      and 0 == r.db('qv').table('interface').filter({'idipaddress':idipaddress}).count().run(g.rdb_conn) \
#      and 0 == r.db('qv').table('ipaddress').filter({'parent':idipaddress}).count().run(g.rdb_conn):
#    r.db('qv').table('ipaddress').get(idipaddress).delete().run(g.rdb_conn)
#    flash('address deleted')
#  else:
#    flash('address in use, not deleted')
  selection = models.TableIpAddress.query.get(idipaddress)
  if models.TableIpAddress.query.filter(TableIpAddress.parent == selection.idipaddress ).count():
    flash( 'ipaddress has child associations')
    flash( 'ipaddress not deleted')
  else:
    db.session.delete(selection)
    db.session.commit()
    flash( 'ipaddress deleted')
    
  return redirect( url_for( 'ipaddresses' ) )

