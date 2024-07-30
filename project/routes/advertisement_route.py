from __main__ import app, db

from flask_login import current_user
from flask import render_template, redirect, request

from models import influencers as Influencers
from models import advertisements as Advertisements
from models import campaigns as Campaigns


@app.route("/advertisements")
def advertisements_index():
    if not current_user.is_authenticated:
        return redirect("/")

    advertisements = Advertisements.Advertisement.query.all()
    advertisements = [
        a for a in advertisements if a.campaign.sponsor_id == current_user.id
    ]
    pending_advertisements = [
        a
        for a in advertisements
        if a.status != "accepted"
        and a.status != "rejected"
        and not "Influencer".lower() in a.status.lower()
    ]
    rejected_advertisements = [a for a in advertisements if a.status == "rejected"]
    accepted_advertisements = [a for a in advertisements if a.status == "accepted"]
    review_negotiation_advertisements = [
        a for a in advertisements if "Influencer" in a.status
    ]

    message = None

    if "message" in request.args:
        message = request.args["message"]

    if current_user.role == "sponsor":
        return render_template(
            "sponsor/advertisements/index.html",
            role="sponsor",
            pending_advertisements=pending_advertisements,
            review_negotiation_advertisements=review_negotiation_advertisements,
            rejected_advertisements=rejected_advertisements,
            accepted_advertisements=accepted_advertisements,
            message=message,
        )

    return render_template("")


@app.route("/advertisements/create", methods=["GET", "POST"])
def create_advertisement():
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        if request.method == "POST":
            message = request.form["message"]
            requirements = request.form["requirements"]
            payment_amount = request.form["amount"]
            influencer_id = request.form["influencer"]
            campaign_id = request.form["campaign"]

            if int(influencer_id) == 0:
                influencer_id = -1

            advertisement = Advertisements.Advertisement(
                influencer_id=influencer_id,
                campaign_id=campaign_id,
                messages=message,
                requirements=requirements,
                payment_amount=payment_amount,
                flagged=False,
                status="pending",
            )

            db.session.add(advertisement)
            db.session.commit()

            return redirect("/advertisements")

        influencer = (
            request.args["influencer"] if "influencer" in request.args else None
        )
        print(influencer)
        influencers = Influencers.Influencer.query.all()
        campaigns = Campaigns.Campaign.query.filter_by(sponsor_id=current_user.id).all()
        return render_template(
            "sponsor/advertisements/create.html",
            role="sponsor",
            influencers=influencers,
            campaigns=campaigns,
            hire_influencer=str(influencer),
        )

    return render_template("")


@app.route("/advertisements/<int:id>", methods=["GET", "POST"])
def edit_advertisements(id):
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        influencers = Influencers.Influencer.query.all()
        campaigns = Campaigns.Campaign.query.filter_by(sponsor_id=current_user.id).all()
        advertisement = Advertisements.Advertisement.query.filter_by(id=id).first()

        if not advertisement:
            return render_template(
                "sponsor/advertisements/edit.html",
                role="sponsor",
                message="Advertisement not found",
            )

        if not advertisement.campaign.sponsor_id == current_user.id:
            return render_template(
                "sponsor/advertisements/index.html",
                role="sponsor",
                message="You don't have enough permissions to edit the advertisement",
            )

        if request.method == "POST":
            message = request.form["message"]
            requirements = request.form["requirements"]
            payment_amount = request.form["amount"]
            influencer_id = request.form["influencer"]
            campaign_id = request.form["campaign"]

            advertisement.messages = message
            advertisement.requirements = requirements
            advertisement.payment_amount = payment_amount
            advertisement.influencer_id = influencer_id
            advertisement.campaign_id = campaign_id
            advertisement.status = "pending"

            db.session.commit()

            return redirect("/advertisements")

        return render_template(
            "sponsor/advertisements/edit.html",
            role="sponsor",
            influencers=influencers,
            campaigns=campaigns,
            advertisement=advertisement,
        )

    return render_template("/")


@app.route("/advertisements/<int:id>/delete")
def delete_advertisement(id):
    if not current_user.is_authenticated:
        return redirect("/")

    if current_user.role == "sponsor":
        advertisement = Advertisements.Advertisement.query.filter_by(id=id).first()

        if not advertisement:
            return redirect('/advertisements?message="Advertisement does not exist!"')

        if not advertisement.campaign.sponsor_id == current_user.id:
            return redirect('/advertisements?message="Not enough permissions"')

        db.session.delete(advertisement)
        db.session.commit()

        return redirect("/advertisements")


@app.route("/advertisements/requests")
def advertisements_request():
    if not current_user.is_authenticated:
        return redirect("/influencer/login")

    message = request.args.get("message")

    advertisements = (
        Advertisements.Advertisement.query.filter(
            Advertisements.Advertisement.influencer_id == current_user.id
        )
        .filter(Advertisements.Advertisement.status != "accepted")
        .filter(Advertisements.Advertisement.status != "rejected")
        .all()
    )

    return render_template(
        "influencer/advertisements/requests.html",
        advertisements=advertisements,
        role="influencer",
        message=message,
    )


@app.route("/advertisement/<string:advertisement_id>/negotiate")
def negotiate_by_influencer(advertisement_id):
    if not current_user.is_authenticated:
        return redirect("/")

    advertisement = Advertisements.Advertisement.query.filter_by(
        id=advertisement_id
    ).first()

    if not advertisement:
        return redirect('/advertisements/requests?message="No advertisement exist"')

    if not advertisement.influencer_id == current_user.id:
        return redirect(
            '/advertisements/requests?message="You do not have enough permissions"'
        )

    negotiatedAmount = request.args["negotiatedAmount"]

    advertisement.payment_amount = negotiatedAmount
    advertisement.status = "Negotiated By Influencer"

    db.session.commit()

    return redirect("/advertisements/all#pending")


@app.route("/advertisement/<string:advertisement_id>/reject")
def rejected_by_influencer(advertisement_id):
    if not current_user.is_authenticated:
        return redirect("/")

    advertisement = Advertisements.Advertisement.query.filter_by(
        id=advertisement_id
    ).first()

    if not advertisement:
        return redirect('/advertisements/requests?message="No advertisement exist"')

    if not advertisement.influencer_id == current_user.id:
        return redirect(
            '/advertisements/requests?message="You do not have enough permissions"'
        )

    if advertisement.campaign.visibility.lower() == "public":
        advertisement.influencer_id = -1
        advertisement.status = "pending"
    else:
        advertisement.status = "rejected"

    db.session.commit()

    return redirect("/advertisements/all#rejected")


@app.route("/advertisement/<string:advertisement_id>/accept")
def accepted_by_influencer(advertisement_id):
    if not current_user.is_authenticated:
        return redirect("/")

    advertisement = Advertisements.Advertisement.query.filter_by(
        id=advertisement_id
    ).first()

    if not advertisement:
        return redirect('/advertisements/requests?message="No advertisement exist"')

    if not advertisement.influencer_id == current_user.id:
        return redirect(
            '/advertisements/requests?message="You do not have enough permissions"'
        )

    advertisement.status = "accepted"

    db.session.commit()

    return redirect("/advertisements/requests#accepted")


# Sponsor requests accept, decline and negotiate
@app.route("/sponsor/advertisement/<string:advertisement_id>/negotiate")
def negotiate_by_sponsor(advertisement_id):
    if not current_user.is_authenticated:
        return redirect("/")

    advertisement = Advertisements.Advertisement.query.filter_by(
        id=advertisement_id
    ).first()

    if not advertisement:
        return redirect('/advertisements/requests?message="No advertisement exist"')

    if not advertisement.campaign.sponsor_id == current_user.id:
        return redirect(
            '/advertisements/requests?message="You do not have enough permissions"'
        )

    negotiatedAmount = request.args["negotiatedAmount"]

    advertisement.payment_amount = negotiatedAmount
    advertisement.status = "Negotiated By Sponsor"
    db.session.commit()

    return redirect("/advertisements")


@app.route("/sponsor/advertisement/<string:advertisement_id>/reject")
def rejected_by_sponsor(advertisement_id):
    if not current_user.is_authenticated:
        return redirect("/")

    advertisement = Advertisements.Advertisement.query.filter_by(
        id=advertisement_id
    ).first()

    if not advertisement:
        return redirect('/advertisements/requests?message="No advertisement exist"')

    if not advertisement.influencer_id == current_user.id:
        return redirect(
            '/advertisements/requests?message="You do not have enough permissions"'
        )

    advertisement.status = "rejected"

    db.session.commit()

    return redirect("/advertisements")


@app.route("/sponsor/advertisement/<string:advertisement_id>/accept")
def accepted_by_sponsor(advertisement_id):
    if not current_user.is_authenticated:
        return redirect("/")

    advertisement = Advertisements.Advertisement.query.filter_by(
        id=advertisement_id
    ).first()

    if not advertisement:
        return redirect('/advertisements/requests?message="No advertisement exist"')

    if not advertisement.campaign.sponsor_id == current_user.id:
        return redirect(
            '/advertisements/requests?message="You do not have enough permissions"'
        )

    advertisement.status = "accepted"

    db.session.commit()

    return redirect("/advertisements/requests")


@app.route("/advertisements/all")
def show_influencers_advertisements():
    if not current_user.is_authenticated:
        return redirect("/")

    advertisements = Advertisements.Advertisement.query.all()
    advertisements = [a for a in advertisements if a.influencer_id == current_user.id]
    pending_advertisements = [
        a for a in advertisements if a.status != "accepted" and a.status != "rejected"
    ]
    rejected_advertisements = [a for a in advertisements if a.status == "rejected"]
    accepted_advertisements = [a for a in advertisements if a.status == "accepted"]
    review_negotiation_advertisements = [
        a for a in advertisements if "Negotiated" in a.status and "Sponsor" in a.status
    ]

    message = None

    if "message" in request.args:
        message = request.args["message"]

    if current_user.role == "influencer":
        return render_template(
            "influencer/advertisements/index.html",
            role="influencer",
            pending_advertisements=pending_advertisements,
            review_negotiation_advertisements=review_negotiation_advertisements,
            rejected_advertisements=rejected_advertisements,
            accepted_advertisements=accepted_advertisements,
            message=message,
        )

    return render_template("")


@app.route("/public/advertisements")
def show_public_advertisements():
    if not current_user.is_authenticated:
        return redirect("/")

    campaigns = Campaigns.Campaign.query.filter_by(visibility="public").all()
    advertisements = []

    for c in campaigns:
        ads = c.advertisements
        for ad in ads:
            if ad.status == "pending":
                advertisements += [ad]

    print(advertisements)
    return render_template(
        "influencer/advertisements/public.html",
        role="influencer",
        advertisements=advertisements,
        user=current_user,
    )


@app.route("/advertisements/apply/<int:ad_id>")
def apply_for_public_ad(ad_id):
    influencer_id = current_user.id
    if not current_user.is_authenticated:
        return redirect("/")

    advertisement = Advertisements.Advertisement.query.filter_by(id=ad_id).first()

    if not advertisement:
        return redirect("/")

    if advertisement.status == "accepted" or advertisement.status == "flagged":
        return redirect("/")

    advertisement.influencer_id = influencer_id
    advertisement.status = "Applied By Influencer"

    db.session.commit()

    return redirect("/advertisements/all")


@app.route("/advertisements/negotiate/<int:advertisement_id>", methods=["GET", "POST"])
def negotiate_public(advertisement_id):
    if not current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        advertisement = Advertisements.Advertisement.query.filter_by(
            id=advertisement_id
        ).first()

        if not advertisement:
            return redirect("/")

        advertisement.status = "Applied By Influencer"
        advertisement.influencer_id = current_user.id
        advertisement.payment_amount = request.form["amount"]

        db.session.commit()

        return redirect("/advertisements/all")

    return render_template(
        "influencer/advertisements/negotiate_public.html", role="influencer"
    )
