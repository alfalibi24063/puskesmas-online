from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

app.config['SECRET_KEY'] = 'abi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puskesmas.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

from pasien.routes import rpasien
app.register_blueprint(rpasien)