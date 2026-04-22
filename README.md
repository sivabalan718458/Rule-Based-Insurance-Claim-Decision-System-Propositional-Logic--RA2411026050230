# Insurance Claim Decision Support System (DSS)

## Live Demo
Access the deployed interactive expert system here:
[https://insurance-claim-expert-system-dhfs.onrender.com](https://insurance-claim-expert-system-dhfs.onrender.com)

This live deployment demonstrates the working implementation of the Rule-Based Insurance Claim Decision Support System using Propositional Logic and Forward Chaining Inference with database-backed claim tracking and structured decision reporting.

### AI Lab Assignment – Problem 14
**Rule-Based Insurance Claim Decision System using Propositional Logic**

---

## Problem Description

An insurance company requires an automated system to evaluate whether a claim should be approved, rejected, or marked for manual review based on predefined logical rules. Manual claim processing is time-consuming and inconsistent.

This project implements a **Rule-Based Expert System** using **Propositional Logic** and **Forward Chaining Inference** to support structured insurance claim decision-making.

The system accepts claim-related facts as user input and applies inference rules to generate explainable decisions along with risk classification and confidence scoring.

---

## System Architecture

The application follows a modular Expert System architecture:

- **Knowledge Base** → Logical rules representing insurance policies (`rule_engine.py`)
- **Inference Engine** → Forward chaining decision execution
- **Explanation Engine** → Transparent reasoning trace (`explanation_engine.py`)
- **Risk Classification Module** → Confidence scoring & eligibility evaluation (`risk_classifier.py`)
- **Database Layer** → SQLAlchemy ORM storage (`models.py`)
- **Presentation Layer** → Flask UI using HTML, CSS, JavaScript

---

## Database Schema

### User Table
Stores authentication and identity information:
- `id` – Primary Key
- `name` – Full Name
- `username` – Unique Login ID
- `password` – Secure hashed credential
- `created_at` – Account creation timestamp

### Claim Table
Stores evaluation history and inference results:
- `id` – Primary Key
- `user_id` – Foreign Key reference
- `claim_type` – Vehicle / Health / Property / Travel
- `policy_active`
- `documents_valid`
- `incident_reported`
- `policy_expired`
- `verification_pending`
- `fraud_suspected`
- `decision`
- `risk_level`
- `confidence_score`
- `timestamp`

---

## Algorithm Used

### Propositional Logic
Knowledge is represented using Boolean facts and implication rules:

**Example:**
- `Policy Active ∧ Documents Valid ∧ Incident Reported → Claim Approved`
- `Fraud Suspected → Claim Rejected`
- `Verification Pending → Manual Review Required`

### Forward Chaining Inference
The system begins with user-provided facts and iteratively evaluates matching rules until a final decision is reached.

**Inference Flow:**
`User Inputs → Fact Base Creation → Rule Matching → Decision Generation`

---

## Features

- Secure User Authentication (Hashed Passwords)
- Rule-Based Claim Evaluation Engine
- Forward Chaining Logical Inference
- Explainable Decision Insights Dashboard
- Risk Classification with Confidence Score
- Claim Eligibility Meter Visualization
- Claim History Tracking (Database-backed)
- Structured PDF Audit Report Generation
- SQLite Database with PostgreSQL Migration Support

---

## Execution Steps

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
python app.py
```

### 3. Database creation
The SQLite database (`instance/database.db`) is automatically generated during the first execution of the application.

---

## Sample Output

**Example Input Facts:**
- Policy Active = TRUE
- Documents Valid = TRUE
- Incident Reported = TRUE
- Fraud Suspected = FALSE
- Verification Pending = FALSE

**Rule Applied:**
`IF policy_active AND documents_valid AND incident_reported THEN Approve Claim`

**Final Decision:**
`CLAIM APPROVED`

**Risk Classification:**
`LOW RISK` (Confidence Score: High)

---

## Technologies Used

### Backend
- Flask
- SQLAlchemy ORM
- SQLite Database

### Frontend
- HTML
- CSS
- JavaScript

### Reporting
- ReportLab PDF Generator

---

## PostgreSQL Migration Support

To switch from SQLite to PostgreSQL:
```bash
set DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```
The application automatically connects using SQLAlchemy configuration.

---

## Conclusion

This project demonstrates the implementation of a Rule-Based Expert System using Propositional Logic and Forward Chaining Inference for automated insurance claim evaluation.

The system improves transparency, consistency, and efficiency of claim decision-making while providing explainable reasoning and structured audit reporting.
