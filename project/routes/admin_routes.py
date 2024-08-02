from __main__ import app, db

from flask_login import current_user, login_user
from flask import redirect, render_template, request
from flask_bcrypt import Bcrypt

from models import users as Users
from models import advertisements as Advertisements

bcrypt = Bcrypt(app)


@app.route('/admin', methods=['GET', 'POST'])
def login_admin():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = Users.Users.query.filter_by(username=username).first()

        if not user:
            return redirect("/admin?message=User%20does%20not%20exist")

        if not bcrypt.check_password_hash(user.password, password):
            return redirect("/admin?message=Incorrect%20password")

        if user.role != "admin":
            return redirect("/admin?message=Not%20enough%20permissions")

        login_user(user)
        return redirect('/')

    message = request.args["message"] if "message" in request.args else None
    return render_template("admin/login.html.jinja", role="admin", message=message)


@app.route('/admin/advertisements')
def show_all_advertisements():
    if not current_user.is_authenticated:
        return redirect("/")

    advertisements = Advertisements.Advertisement.query.all()

    message = request.args["message"] if "message" in request.args else None
    success = request.args["success"] if "success" in request.args else None

    print(success)

    return render_template("admin/advertisements.html.jinja", role="admin", advertisements=advertisements,
                           success=success,
                           message=message)


@app.route('/admin/advertisement/<int:advertisement_id>/flag')
def flag_advertisement(advertisement_id):
    if not current_user.is_authenticated:
        return redirect("/")

    if not current_user.role == "admin":
        return redirect("/")

    advertisement = Advertisements.Advertisement.query.filter_by(id=advertisement_id).first()

    if not advertisement:
        return redirect("/admin/advertisements?message=Advertisement%20does%20not%20exist")

    advertisement.flagged = True
    db.session.commit()

    return redirect("/admin/advertisements?message=Successfully%20flagged%20advertisement&success=true")


@app.route('/admin/advertisement/<int:advertisement_id>/unflag')
def unflag_advertisement(advertisement_id):
    if not current_user.is_authenticated:
        return redirect("/")

    if not current_user.role == "admin":
        return redirect("/")

    advertisement = Advertisements.Advertisement.query.filter_by(id=advertisement_id).first()

    if not advertisement:
        return redirect("/admin/advertisements?message=Advertisement%20does%20not%20exist")

    advertisement.flagged = False
    db.session.commit()

    return redirect("/admin/advertisements?message=Successfully%20unflagged%20advertisement&success=true")
