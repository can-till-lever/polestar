ORGANIZATION_ID = 'QVSL'
ORGANIZATION_NAME = 'QuoVadis Services Limited'

CSRF_ENABLED = True  # cross site request forgery prevention, http://en.wikipedia.org/wiki/Cross-site_request_forgery
SECRET_KEY = 'PoleSt*rL!v3s'  #create a cryptographic token that is used to validate a form

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }
    ]

# http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html
# postgresql+pypostgresql://user:password@host:port/dbname[?key=value&key=value...]

SQLALCHEMY_DATABASE_URI = "postgresql+pypostgresql://polestar:starring@127.0.0.1/polestar"
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository') #store the SQLAlchemy-migrate data files.

SQLALCHEMY_COMMIT_ON_TEARDOWN = True  #enable automatic commits of database changes at the end of each request
#SQLALCHEMY_RECORD_QUERIES = True

