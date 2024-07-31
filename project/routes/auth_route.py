from __main__ import app, db

from models import categories as Categories
from models import users as Users
from models import influencers as Influencers
from models import sponsors as Sponsors

from flask import redirect, render_template, request
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_user, logout_user

bcrypt = Bcrypt(app)

# Sponsor Auth routes
@app.route("/sponsor/register", methods=["POST", "GET"])
def sponsor_registration():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"])
        industry = request.form["industry"]
        budget = request.form["budget"]

        if Users.Users.query.filter_by(username=username).first():
            return render_template(
                "sponsor/auth/register.html",
                message="Username is already taken",
            )

        user = Users.Users(username=username, password=password, role="sponsor")
        db.session.add(user)
        db.session.commit()

        sponsor = Sponsors.Sponsors(
            id=user.id, name=name, industry=industry, budget=budget
        )
        db.session.add(sponsor)
        db.session.commit()

        return redirect("/sponsor/login")

    return render_template("sponsor/auth/register.html")


@app.route("/sponsor/login", methods=["GET", "POST"])
def sponsor_login():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = Users.Users.query.filter_by(username=username).first()

        if not user:
            return render_template(
                "sponsor/auth/login.html", message="Username not found"
            )

        if user.role != "sponsor":
            return render_template(
                "sponsor/auth/login.html", message="Sponsor not found"
            )

        if not bcrypt.check_password_hash(user.password, password):
            return render_template(
                "sponsor/auth/login.html", message="Password is incorrect"
            )

        login_user(user)
        return redirect("/")

    return render_template("/sponsor/auth/login.html")


# Influencer Auth Routes
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

        if Users.Users.query.filter_by(username=username).first():
            return render_template(
                "influencer/auth/register.html",
                message="Username is already taken",
                categories=categories,
            )

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


@app.route("/influencer/login", methods=["GET", "POST"])
def influencer_login():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = Users.Users.query.filter_by(username=username).first()

        if not user:
            return render_template(
                "influencer/auth/login.html", message="Username not found"
            )

        if user.role != "influencer":
            return render_template(
                "influencer/auth/login.html", message="Influencer not found"
            )

        if not bcrypt.check_password_hash(user.password, password):
            return render_template(
                "influencer/auth/login.html", message="Password is incorrect"
            )

        login_user(user)
        return redirect("/")

    return render_template("/influencer/auth/login.html")


# Logout route
@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect("/")


# Create Category Api
@app.route("/category/create/<string:category_name>")
def create_category(category_name):
    if category_name == "":
        return ""

    category = Categories.Category(name=category_name)
    db.session.add(category)
    db.session.commit()

    return ""
