from __main__ import app, db

from flask import redirect, render_template, request
from flask_login import current_user

from datetime import datetime

from models import campaigns as Campaigns
from models import advertisements as Advertisements


@app.route("/campaigns")
def show_campaigns():
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        campaigns = Campaigns.Campaign.query.filter_by(sponsor_id=current_user.id).all()

        message = None
        if "message" in request.args:
            message = request.args['message']

        return render_template("sponsor/campaigns/index.html.jinja", role="sponsor", campaigns=campaigns,
                               message=message)

    return render_template("")


@app.route('/campaigns/create', methods=['GET', 'POST'])
def create_campaign():
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        if request.method == "POST":
            name = request.form['name']
            description = request.form['description']
            start_date = request.form['start-date']
            end_date = request.form['end-date']
            goals = request.form['goals']
            budget = request.form['budget']
            visibility = request.form['visibility']

            date_format = '%Y-%m-%d'
            start_date = datetime.strptime(start_date, date_format)
            end_date = datetime.strptime(end_date, date_format)

            if start_date > end_date:
                return render_template("sponsor/campaigns/create.html.jinja", role="sponsor",
                                       message="Select valid dates")

            campaign = Campaigns.Campaign(
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                goals=goals,
                visibility=visibility,
                budget=budget,
                sponsor_id=current_user.id,
                flagged=False
            )

            db.session.add(campaign)
            db.session.commit()

            return redirect("/campaigns")

        return render_template("sponsor/campaigns/create.html.jinja", role="sponsor")

    return render_template('')


@app.route("/campaigns/<int:campaign_id>", methods=["GET", "POST"])
def edit_campaign(campaign_id):
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        campaign = Campaigns.Campaign.query.filter_by(id=campaign_id).first()

        if not campaign:
            return render_template("sponsor/campaigns/edit.html.jinja", role="sponsor",
                                   message="Advertisement not found")

        if not campaign.sponsor_id == current_user.id:
            return render_template("sponsor/campaigns/index.html.jinja", role="sponsor",
                                   message="You don't have enough permissions to edit the advertisement")

        if request.method == "POST":
            name = request.form['name']
            description = request.form['description']
            start_date = request.form['start-date']
            end_date = request.form['end-date']
            goals = request.form['goals']
            budget = request.form['budget']
            visibility = request.form['visibility']

            date_format = '%Y-%m-%d'
            start_date = datetime.strptime(start_date, date_format)
            end_date = datetime.strptime(end_date, date_format)

            campaign.name = name
            campaign.description = description
            campaign.start_date = start_date
            campaign.end_date = end_date
            campaign.goals = goals
            campaign.budget = budget
            campaign.visibility = visibility
            db.session.commit()

            return redirect("/campaigns")

        return render_template("sponsor/campaigns/edit.html.jinja", role="sponsor", campaign=campaign)

    return render_template("/")


@app.route("/campaigns/<int:id>/delete")
def delete_campaign(id):
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        campaign = Campaigns.Campaign.query.filter_by(id=id).first()

        if not campaign:
            return redirect('/campaigns?message="Campaign does not exist!"')

        if not campaign.sponsor_id == current_user.id:
            return redirect('/campaigns?message="Permission denied"')

        advertisements = Advertisements.Advertisement.query.filter_by(campaign_id=id).all()

        for ad in advertisements:
            db.session.delete(ad)
            db.session.commit()

        db.session.delete(campaign)
        db.session.commit()

        return redirect('/campaigns')

    return render_template('')
