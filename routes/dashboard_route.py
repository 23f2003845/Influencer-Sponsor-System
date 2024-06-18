from __main__ import app

from models import advertisements as Advertisements
from models import campaigns as Campaigns

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

        campaigns = Campaigns.Campaign.query.all()


        return render_template(
            "sponsor/dashboard.html",
            role="sponsor",
            advertisements=advertisements,
            campaigns=campaigns,
        )

    return render_template("influencer/dashboard.html", role="influencer")
