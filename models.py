from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    claim_type = db.Column(db.String(50), nullable=False)
    
    # Propositional Logic Facts
    policy_active = db.Column(db.Boolean, default=False)
    documents_valid = db.Column(db.Boolean, default=False)
    incident_reported = db.Column(db.Boolean, default=False)
    policy_expired = db.Column(db.Boolean, default=False)
    verification_pending = db.Column(db.Boolean, default=False)
    fraud_suspected = db.Column(db.Boolean, default=False)
    
    # Results
    decision = db.Column(db.String(50))
    risk_level = db.Column(db.String(20))
    confidence_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref=db.backref('claims', lazy=True))
