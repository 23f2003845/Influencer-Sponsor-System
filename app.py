from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()

# App configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SECRET_KEY"] = "MYSUPERSECRETKEY"

db = SQLAlchemy()
db.init_app(app)

from models import users
from models import influencers
from models import campaigns
from models import sponsors
from models import advertisements

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return users.Users.query.get(user_id)


from routes import auth

if __name__ == "__main__":
    app.run(debug=True)
