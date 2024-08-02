from __main__ import app

from models import advertisements as Advertisements
from models import campaigns as Campaigns
from models import influencers as Influencers
from models import users as Users

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

        campaigns = Campaigns.Campaign.query.filter_by(sponsor_id=current_user.id).all()

        return render_template(
            "sponsor/dashboard.html.jinja",
            role="sponsor",
            advertisements=advertisements,
            campaigns=campaigns,
        )

    if current_user.role == "admin":
        users = Users.Users.query.all()
        advertisements = Advertisements.Advertisement.query.all()
        campaigns = Campaigns.Campaign.query.all()

        sponsors = [u for u in users if u.role == "sponsor"]
        influencers = [u for u in users if u.role == "influencer"]

        sponsor_count = len(sponsors)
        influencer_count = len(influencers)
        advertisement_count = len(advertisements)
        campaign_count = len(campaigns)

        return render_template("admin/dashboard.html.jinja", role="admin", sponsor_count=sponsor_count,
                               influencer_count=influencer_count, advertisement_count=advertisement_count,
                               campaign_count=campaign_count)

    influencer = Influencers.Influencer.query.filter_by(id=current_user.id).first()

    return render_template("influencer/dashboard.html.jinja", role="influencer", influencer=influencer)
