from __main__ import app

from models import advertisements as Advertisements
from models import campaigns as Campaigns
from models import influencers as Influencers

from flask import redirect, render_template
from flask_login import current_user


@app.route("/")
def homepage():
    if not current_user.is_authenticated:
        return redirect("/sponsor/register")

    if current_user.role == "sponsor":
        advertisements = Advertisements.Advertisement.query.all()
        advertisements = [
            a for a in advertisements if a.campaign.sponsor_id == current_user.id
        ]

        campaigns = Campaigns.Campaign.query.filter_by(sponsor_id = current_user.id).all()


        return render_template(
            "sponsor/dashboard.html",
            role="sponsor",
            advertisements=advertisements,
            campaigns=campaigns,
        )

    influencer = Influencers.Influencer.query.filter_by(id=current_user.id).first()


    return render_template("influencer/dashboard.html", role="influencer", influencer=influencer)
