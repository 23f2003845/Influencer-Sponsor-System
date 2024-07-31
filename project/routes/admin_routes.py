from __main__ import app, db

from flask_login import current_user, login_user
from flask import redirect, render_template, request
from flask_bcrypt import Bcrypt

from models import users as Users

bcrypt = Bcrypt(app)


@app.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = Users.Users.query.filter_by(username=username).first()

        if not user:
            return redirect("/admin/login?message=User%20does%20not%20exist")

        if not bcrypt.check_password_hash(user.password, password):
            return redirect("/admin/login?message=Incorrect%20password")

        if user.role != "admin":
            return redirect("/admin/login?message=Not%20enough%20permissions")

        login_user(user)
        return redirect('/')

    message = request.args["message"] if "message" in request.args else None
    return render_template("admin/login.html", role="admin", message=message)
