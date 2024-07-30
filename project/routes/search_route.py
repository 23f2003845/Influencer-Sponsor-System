from __main__ import app

from flask import redirect, render_template, request
from flask_login import current_user

from models import influencers as Influencers
from models import categories as Categories
from models import users as Users


@app.route("/search")
def influencer_search():
    if not current_user.is_authenticated:
        return redirect("/")

    if "search" not in request.args:
        keyword = ""
    else:
        keyword = request.args["search"]

    keyword = keyword.lower()

    influencers = (
        Influencers.Influencer.query.join(
            Users.Users, Users.Users.id == Influencers.Influencer.id
        )
        .add_columns(
            Users.Users.username,
            Influencers.Influencer.name,
            Influencers.Influencer.bio,
            Influencers.Influencer.category_id,
        )
        .all()
    )

    categories_records = Categories.Category.query.all()

    categories = {}

    for c in categories_records:
        categories[c.id] = c.name.lower()

    influencer_index = [
        influencer
        for influencer in influencers
        if (keyword in influencer.name.lower())
        or (keyword in influencer.bio.lower())
        or (keyword in categories[influencer.category_id])
        or (keyword in influencer.username)
    ]

    return render_template(
        "sponsor/search.html",
        role="sponsor",
        influencers=influencer_index,
        categories=categories,
    )
