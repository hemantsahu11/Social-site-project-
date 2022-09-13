from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask import current_app
# from flask_cors import CORS

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
# CORS(app)
#             allow_headers=['content-type', 'accept', 'Authorization',
#                      'user-agent', 'sec-ch-ua', 'sech-ch-ua-mobile',
#                      'sech-ch-ua-platform', 'referer', 'sec-fetch-mode',
#                      'sec-fetch-dest', 'sec-fetch-site', 'accept-encoding',
#                      'accept-language'])
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
jwt = JWTManager(app)
app.app_context().push()
app.test_request_context().push()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abcd@localhost:5432/flask_db'
app.config['SECRET_KEY']='8eb7d7067ddaea5469f2149b'

from application import routes