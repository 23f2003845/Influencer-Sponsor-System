from __main__ import app, db

from flask_login import current_user
from flask import render_template, redirect, request

from models import influencers as Influencers
from models import advertisements as Advertisements
from models import campaigns as Campaigns

@app.route('/advertisements')
def advertisements_index():
    if not current_user.is_authenticated:
        return redirect("/")

    advertisements =  Advertisements.Advertisement.query.all()
    advertisements = [
         a for a in advertisements if a.campaign.sponsor_id == current_user.id
    ]
    if current_user.role == "sponsor":
        return render_template("sponsor/advertisements/index.html", role="sponsor", advertisements=advertisements)

    return render_template("")

@app.route("/advertisements/create", methods=['GET', 'POST'])
def create_advertisement():
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        if request.method == "POST":
            message = request.form['message']
            requirements = request.form['requirements']
            payment_amount = request.form['amount']
            influencer_id = request.form['influencer']
            campaign_id = request.form['campaign']

            advertisement = Advertisements.Advertisement(
                influencer_id = influencer_id,
                campaign_id = campaign_id,
                messages=message,
                requirements = requirements,
                payment_amount = payment_amount,
                flagged = False,
                status = 'pending'
            )

            db.session.add(advertisement)
            db.session.commit()

            return redirect('/advertisements')

        influencers = Influencers.Influencer.query.all()
        campaigns = Campaigns.Campaign.query.filter_by(sponsor_id = current_user.id).all()
        return render_template("sponsor/advertisements/create.html", role="sponsor", influencers=influencers, campaigns=campaigns)

    return render_template("")