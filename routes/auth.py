from __main__ import app

from flask import render_template
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/influencer/register")
def influencer_registration():
    return render_template("influencer/auth/register.html")
