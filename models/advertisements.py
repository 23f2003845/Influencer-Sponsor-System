from __main__ import db


class Advertisement(db.Model):
    __tablename__ = "advertisement"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    influencer_id = db.Column(
        db.Integer, db.ForeignKey("influencer.id"), nullable=False
    )
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"), nullable=False)
    messages = db.Column(db.String(255), nullable=False)
    requirements = db.Column(db.String(255), nullable=False)
    payment_amount = db.Column(db.Integer, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    accepted = db.Column(db.Boolean, default=False)
