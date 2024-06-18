from flask_api import app, db
from flask_api.models import User, Manager, Brand, Card


app.app_context().push()
all_users       = User.query.all()
all_clients     = User.query.filter_by(manager=None).order_by(User.id.desc())
all_clients     = User.query.filter(User.manager.__eq__(None)).order_by(User.id.desc())
all_managers    = User.query.filter(User.manager.__ne__(None)).order_by(User.id.desc())
all_brands      = Brand.query.all()
all_cards       = Card.query.all()

query_response = all_cards


for record in query_response:
    print(record.log())
