from app import db
from main import app_obj

app_obj.app_context().push()

db.drop_all()
db.create_all()
