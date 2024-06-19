from __main__ import app 

from flask_login import current_user
from flask import render_template

from models import users as Users
from models import influencers as Influencers
from models import categories as Categories

@app.route('/influencer/<string:username>/profile')
def show_influencer_profile(username):

    if not current_user.is_authenticated: 
        role = ""
    else:
        role = current_user.role

    user = Users.Users.query.filter_by(username=username).first()
    if not user:
        return render_template("influencer/profile.html", role=role, message = "Influencer not found")

    influencer = Influencers.Influencer.query.filter_by(id = user.id).first()
    category = Categories.Category.query.filter_by(id = influencer.category_id).first()

    if not category:
        return render_template("influencer/profile.html", role=role, message = "Influencer not found")
        
    recommended = Influencers.Influencer.query.join(Users.Users, Users.Users.id == Influencers.Influencer.id).add_columns(Influencers.Influencer.id, Influencers.Influencer.name, Influencers.Influencer.reach, Users.Users.username, Influencers.Influencer.category_id).filter(Influencers.Influencer.category_id == category.id).all()

    successful_advertisement_count = 10
    happy_clients_count = 5
    return render_template('influencer/profile.html', 
                                role=role, 
                                influencer=influencer, 
                                username=username, 
                                category=category,
                                successful_advertisement_count=successful_advertisement_count, 
                                happy_clients_count=happy_clients_count,
                                recommended = recommended
                            )