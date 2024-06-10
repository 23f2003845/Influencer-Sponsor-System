from __main__ import app, db

from models import categories as Categories
from models import users as Users
from models import influencers as Influencers

from flask import redirect, render_template, request
from flask_bcrypt import Bcrypt
from flask_login import current_user

bcrypt = Bcrypt(app)


@app.route("/influencer/register", methods=["POST", "GET"])
def influencer_registration():
    if current_user.is_authenticated:
        return redirect("/")

    categories = Categories.Category.query.all()
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"])
        bio = request.form["bio"]
        category = request.form["category"]
        reach = request.form["reach"]
        niche = request.form["niche"]

        user = Users.Users(username=username, password=password, role="influencer")
        db.session.add(user)
        db.session.commit()

        influencer = Influencers.Influencer(
            id=user.id,
            name=name,
            bio=bio,
            category_id=category,
            reach=reach,
            niche=niche,
        )
        db.session.add(influencer)
        db.session.commit()

        return redirect("/influencer/login")

    return render_template("influencer/auth/register.html", categories=categories)


@app.route("/category/create/<string:category_name>")
def create_category(category_name):
    if category_name == "":
        return ""

    category = Categories.Category(name=category_name)
    db.session.add(category)
    db.session.commit()

    return ""
