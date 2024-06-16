from __main__ import app

from flask_login import current_user
from flask import render_template, redirect

from models import advertisements as Advertisements

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