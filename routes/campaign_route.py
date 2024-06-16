from __main__ import app

from flask import redirect, render_template
from flask_login import current_user

from models import campaigns as Campaigns

@app.route("/campaigns")
def show_campaigns():
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        campaigns = Campaigns.Campaign.query.filter_by(sponsor_id=current_user.id).all()

        return render_template("sponsor/campaigns/index.html", role="sponsor", campaigns=campaigns)

    return render_template("")