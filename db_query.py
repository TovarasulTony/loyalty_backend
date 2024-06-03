from flask_api import app, db
from flask_api.models import User, Manager, Brand


app.app_context().push()
query_response = Brand.query.all()
print(query_response)

for brand in query_response:
    print(brand.log())
