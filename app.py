import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Claim
from rule_engine import RuleEngine
from risk_classifier import RiskClassifier
from explanation_engine import ExplanationEngine
from report_generator import ReportGenerator
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'insurance_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database on first run
with app.app_context():
    db.create_all()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('register'))

        new_user = User(
            name=name,
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        
        flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch user's claims
    user_claims = Claim.query.filter_by(user_id=session['user_id']).all()
    
    # Calculate stats
    stats = {
        'total': len(user_claims),
        'approved': len([c for c in user_claims if c.decision == 'Approved']),
        'rejected': len([c for c in user_claims if c.decision == 'Rejected']),
        'review': len([c for c in user_claims if "Manual" in c.decision])
    }
    
    # Fetch last 5 claims for reports tab history
    history = Claim.query.filter_by(user_id=session['user_id']).order_by(Claim.timestamp.desc()).limit(5).all()
    
    return render_template('dashboard.html', stats=stats, claims=history)

@app.route('/delete_claim/<int:claim_id>')
@login_required
def delete_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    if claim.user_id != session['user_id']:
        return "Unauthorized", 403
    
    db.session.delete(claim)
    db.session.commit()
    flash('Claim record deleted successfully.')
    return redirect(url_for('dashboard'))

@app.route('/evaluate_claim', methods=['POST'])
@login_required
def evaluate_claim():
    data = request.json
    
    # Process boolean facts
    facts = {
        'policy_active': data.get('policy_active') == 'yes',
        'documents_valid': data.get('documents_valid') == 'yes',
        'incident_reported': data.get('incident_reported') == 'yes',
        'policy_expired': data.get('policy_expired') == 'yes',
        'verification_pending': data.get('verification_pending') == 'yes',
        'fraud_suspected': data.get('fraud_suspected') == 'yes'
    }
    
    # Run Inference Engine
    decision = RuleEngine.evaluate(facts)
    
    # Run Risk Classification
    claim_type = data.get('claim_type')
    confidence_score = RiskClassifier.calculate_confidence_score(
        claim_type,
        facts['policy_active'],
        facts['documents_valid'],
        facts['incident_reported'],
        facts['policy_expired'],
        facts['verification_pending'],
        facts['fraud_suspected']
    )
    risk_level = RiskClassifier.classify(confidence_score)
    
    # Run Eligibility Scoring
    eligibility_score = RiskClassifier.calculate_eligibility_score(facts)
    
    # Generate Structured Explanation
    explanation_data = ExplanationEngine.get_structured_explanation(facts, decision)
    
    # Store in Database
    new_claim = Claim(
        user_id=session['user_id'],
        claim_type=data.get('claim_type'),
        **facts,
        decision=decision,
        risk_level=risk_level,
        confidence_score=confidence_score
    )
    db.session.add(new_claim)
    db.session.commit()
    
    # Store last claim ID in session for report generation
    session['last_claim_id'] = new_claim.id
    
    return jsonify({
        'success': True,
        'data': {
            'id': new_claim.id,
            'decision': decision,
            'risk_level': risk_level,
            'confidence_score': confidence_score,
            'eligibility_score': eligibility_score,
            'explanation_data': explanation_data,
            'timestamp': new_claim.timestamp.strftime('%d %b %H:%M'),
            'claim_type': new_claim.claim_type
        }
    })

@app.route('/generate_report/<int:claim_id>')
@login_required
def generate_report(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    if claim.user_id != session['user_id']:
        return "Unauthorized", 403
        
    user = User.query.get(session['user_id'])
    
    # Re-calculate explanation data for the PDF
    facts = {
        'policy_active': claim.policy_active,
        'documents_valid': claim.documents_valid,
        'incident_reported': claim.incident_reported,
        'policy_expired': claim.policy_expired,
        'verification_pending': claim.verification_pending,
        'fraud_suspected': claim.fraud_suspected
    }
    explanation_data = ExplanationEngine.get_structured_explanation(facts, claim.decision)
    
    report_filename = f"claim_report_{claim_id}.pdf"
    report_path = os.path.join('instance', report_filename)
    
    ReportGenerator.generate_pdf(claim, user, explanation_data, report_path)
    
    return send_file(report_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
