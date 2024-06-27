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

    message = None

    if "message" in request.args:
        message = request.args["message"]

    if current_user.role == "sponsor":
        return render_template("sponsor/advertisements/index.html", role="sponsor", advertisements=advertisements, message=message)

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

        influencer = request.args['influencer'] if 'influencer' in request.args else None
        print(influencer)
        influencers = Influencers.Influencer.query.all()
        campaigns = Campaigns.Campaign.query.filter_by(sponsor_id = current_user.id).all()
        return render_template("sponsor/advertisements/create.html", role="sponsor", influencers=influencers, campaigns=campaigns, hire_influencer=str(influencer))

    return render_template("")

@app.route("/advertisements/<int:id>", methods=["GET", "POST"])
def edit_advertisements(id):
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        influencers = Influencers.Influencer.query.all()
        campaigns = Campaigns.Campaign.query.filter_by(sponsor_id = current_user.id).all()
        advertisement = Advertisements.Advertisement.query.filter_by(id = id).first()

        if not advertisement:
            return render_template("sponsor/advertisements/edit.html", role="sponsor", message="Advertisement not found")

        if not advertisement.campaign.sponsor_id == current_user.id:
            return render_template("sponsor/advertisements/index.html", role="sponsor", message="You don't have enough permissions to edit the advertisement")

        if request.method == "POST":
            message = request.form['message']
            requirements = request.form['requirements']
            payment_amount = request.form['amount']
            influencer_id = request.form['influencer']
            campaign_id = request.form['campaign']

            advertisement.messages = message
            advertisement.requirements = requirements
            advertisement.payment_amount = payment_amount
            advertisement.influencer_id = influencer_id
            advertisement.campaign_id = campaign_id

            db.session.commit()

            return redirect("/advertisements")
 
        return render_template("sponsor/advertisements/edit.html", role="sponsor", influencers=influencers, campaigns = campaigns, advertisement = advertisement)

    return render_template("/")


@app.route("/advertisements/<int:id>/delete")
def delete_advertisement(id):
    if not current_user.is_authenticated:
        return redirect("/")
    
    if current_user.role == "sponsor":
        advertisement = Advertisements.Advertisement.query.filter_by(id = id).first()

        if not advertisement:
            return redirect('/advertisements?message="Advertisement does not exist!"')
        
        if not advertisement.campaign.sponsor_id == current_user.id:
            return redirect('/advertisements?message="Not enough permissions"')

        db.session.delete(advertisement)
        db.session.commit()

        return redirect("/advertisements")