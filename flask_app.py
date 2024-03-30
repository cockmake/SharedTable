from flask import Flask
from flask_cors import CORS

from blue_print import user, admin

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(admin)
CORS(app)
