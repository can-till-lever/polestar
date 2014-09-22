from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from app import app, db, models

from app.forms import FormOrganizationEdit, FormOrganizationAdd

from app.models import TableOrganization

@app.route('/organizations')
def organizations():
  selection = models.TableOrganization.query.order_by(TableOrganization.idorganization).all()
  return render_template( 'organization.html', organizations=selection )

def organization_assign( form, table ):
  table.name = form.name.data
  table.description = form.description.data
  table.asn = form.asn.data
  table.url = form.url.data

@app.route('/organization/add', methods=['GET'])
def organization_add_get():
  form = FormOrganizationAdd()
  return render_template( 'organization_edit.html', form=form, mode='add' )

@app.route('/organization/add', methods=['POST'])
def organization_add_post():
  form = FormOrganizationAdd()
  if form.validate_on_submit():
    # do a query first to see if organization exists, or error on duplicate attempt?
    org = TableOrganization()
    org.idorganization = form.idorganization.data.upper()
    organization_assign( form, org )
    db.session.add( org )
    db.session.commit()
    flash('organization added')
    # what next?  another new one, edit mode, or organization?
    return redirect( url_for( 'organizations' ) )
  else:
    # errors will be reported in the page via form messages
    return render_template( 'organization_edit.html', form=form, mode='add' )

@app.route('/organization/edit/<idorganization>', methods=['GET'])
def organization_edit_get( idorganization ):

  form = FormOrganizationEdit()

  org = models.TableOrganization.query.get(idorganization)
  form.name.data = org.name
  form.description.data = org.description
  form.asn.data = org.asn
  form.url.data = org.url
  return render_template( 'organization_edit.html', org=org, form=form, mode='edit' )

@app.route('/organization/edit/<idorganization>', methods=['POST'])
def organization_edit_post( idorganization ):

  form = FormOrganizationEdit()

  org = models.TableOrganization.query.get(idorganization)
  if form.validate_on_submit():
    organization_assign( form, org )
    db.session.commit()
    flash('organization changes saved')
    return redirect( url_for( 'organizations' ) )
  else:
    # errors will be reported in the page via form messages
    return render_template( 'organization_edit.html', org=org, form=form, mode='edit' )

@app.route('/organization/delete/<idorganization>', methods=['GET'])
def organization_delete(idorganization):
  selection = models.TableOrganization.query.get(idorganization)
  db.session.delete(selection)
  db.session.commit()
  flash('organization deleted')
  return redirect( url_for( 'organizations' ) )
