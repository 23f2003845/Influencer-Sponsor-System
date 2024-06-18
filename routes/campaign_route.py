from __main__ import app, db

from flask import redirect, render_template, request
from flask_login import current_user

from datetime import datetime

from models import campaigns as Campaigns

@app.route("/campaigns")
def show_campaigns():
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        campaigns = Campaigns.Campaign.query.filter_by(sponsor_id=current_user.id).all()

        return render_template("sponsor/campaigns/index.html", role="sponsor", campaigns=campaigns)

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
                return render_template("sponsor/campaigns/create.html", role="sponsor", message="Select valid dates")

            campaign = Campaigns.Campaign(
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                goals=goals,
                visibility=visibility,
                budget=budget,
                sponsor_id = current_user.id,
                flagged=False
            )

            db.session.add(campaign)
            db.session.commit()

            return redirect("/campaigns")

        return render_template("sponsor/campaigns/create.html", role="sponsor")