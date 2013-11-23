import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://caudle:password@localhost/caudledb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

