from __main__ import app, db

from flask_login import current_user
from flask import render_template

from models import users as Users
from models import influencers as Influencers
from models import categories as Categories
from models import advertisements as Advertisements


@app.route("/influencer/<string:username>/profile")
def show_influencer_profile(username):
    if not current_user.is_authenticated:
        role = ""
    else:
        role = current_user.role

    user = Users.Users.query.filter_by(username=username).first()
    if not user:
        return render_template(
            "influencer/profile.html", role=role, message="Influencer not found"
        )

    influencer = Influencers.Influencer.query.filter_by(id=user.id).first()
    category = Categories.Category.query.filter_by(id=influencer.category_id).first()

    if not category:
        return render_template(
            "influencer/profile.html", role=role, message="Influencer not found"
        )

    # recommended = (
    #     Influencers.Influencer.query.join(
    #         Users.Users, Users.Users.id == Influencers.Influencer.id
    #     )
    #     .add_columns(
    #         Influencers.Influencer.id,
    #         Influencers.Influencer.name,
    #         Influencers.Influencer.reach,
    #         Users.Users.username,
    #     )
    #     .filter(Influencers.Influencer.category_id == category.id)
    #     .all()
    # )

    recommended = db.session.query(Influencers.Influencer.id,
                                    Users.Users.username, 
                                    Influencers.Influencer.reach, 
                                    Influencers.Influencer.category_id, 
                                    Influencers.Influencer.name)\
                            .join(Users.Users, Users.Users.id == Influencers.Influencer.id)

    successful_advertisement_count = Advertisements.Advertisement.query.filter_by(influencer_id=user.id).filter_by(status="completed").all()

    happy_clients_count = set()

    for ad in successful_advertisement_count:
        if ad.campaign.sponsor_id not in happy_clients_count:
            happy_clients_count.add(ad.campaign.sponsor_id)

    return render_template(
        "influencer/profile.html",
        role=role,
        influencer=influencer,
        username=username,
        category=category,
        successful_advertisement_count=successful_advertisement_count,
        happy_clients_count=happy_clients_count,
        recommended=recommended,
    )
