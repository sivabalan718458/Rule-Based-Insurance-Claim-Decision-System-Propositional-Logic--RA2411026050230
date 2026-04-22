class RiskClassifier:
    @staticmethod
    def classify(confidence_score):
        if confidence_score >= 80:
            return "LOW RISK"
        elif confidence_score >= 50:
            return "MEDIUM RISK"
        else:
            return "HIGH RISK"

    @staticmethod
    def calculate_confidence_score(
        claim_type,
        policy_active,
        documents_valid,
        incident_reported,
        policy_expired,
        verification_pending,
        fraud_suspected
    ):
        score = 50

        if claim_type == "Vehicle Claim":
            weights = {
                "policy_active": 25,
                "documents_valid": 25,
                "incident_reported": 40,
                "verification_pending": -15,
                "fraud_suspected": -60,
                "policy_expired": -80
            }
        elif claim_type == "Health Claim":
            weights = {
                "policy_active": 30,
                "documents_valid": 45,
                "incident_reported": 10,
                "verification_pending": -25,
                "fraud_suspected": -60,
                "policy_expired": -80
            }
        elif claim_type == "Property Claim":
            weights = {
                "policy_active": 30,
                "documents_valid": 20,
                "incident_reported": 30,
                "verification_pending": -20,
                "fraud_suspected": -70,
                "policy_expired": -80
            }
        elif claim_type == "Travel Claim":
            weights = {
                "policy_active": 40,
                "documents_valid": 25,
                "incident_reported": 20,
                "verification_pending": -20,
                "fraud_suspected": -50,
                "policy_expired": -80
            }
        else:
            weights = {}

        if policy_active:
            score += weights.get("policy_active", 0)
        if documents_valid:
            score += weights.get("documents_valid", 0)
        if incident_reported:
            score += weights.get("incident_reported", 0)
        if verification_pending:
            score += weights.get("verification_pending", 0)
        if fraud_suspected:
            score += weights.get("fraud_suspected", 0)
        if policy_expired:
            score += weights.get("policy_expired", 0)

        score = max(0, min(score, 100))
        return score

    @staticmethod
    def calculate_eligibility_score(facts):
        # Keeps internal meter consistent with core facts
        score = 0
        if facts.get('policy_active'): score += 40
        if facts.get('documents_valid'): score += 30
        if facts.get('incident_reported'): score += 30
        
        # Deductions
        if facts.get('fraud_suspected'): score -= 50
        if facts.get('policy_expired'): score -= 50
        
        return max(0, min(score, 100))
