import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
    os.path.join(BASE_DIR, 'library.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'V\x8cn\xa2\x8d\xfa\xb9\xd3\xb2\xe7\xf77\x87c\xc2\x9a'
