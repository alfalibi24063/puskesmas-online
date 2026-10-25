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
login_manager.login_view = 'rpasien.login'
login_manager.login_message = 'Silakan login terlebih dahulu.'
login_manager.init_app(app)

from pasien.models import Tpasien

@login_manager.user_loader
def load_user(user_id):
    return Tpasien.query.get(int(user_id))


# ===================== Register Blueprint =====================

from pasien.routes import rpasien
from admin import radmin

app.register_blueprint(rpasien)
app.register_blueprint(radmin, url_prefix='/admin')