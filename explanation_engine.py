class ExplanationEngine:
    @staticmethod
    def get_structured_explanation(facts, decision):
        # 1. Fact Base
        facts_display = {
            "Policy Active": facts.get('policy_active'),
            "Documents Valid": facts.get('documents_valid'),
            "Incident Reported": facts.get('incident_reported'),
            "Policy Expired": facts.get('policy_expired'),
            "Verification Pending": facts.get('verification_pending'),
            "Fraud Suspected": facts.get('fraud_suspected')
        }

        # 2. Forward Chaining Trace
        rule_trace = []
        rule_trace.append({"rule": "Checking Policy Expiry", "result": facts.get('policy_expired')})
        if facts.get('policy_expired'):
            matched_rule = "IF policy_expired THEN Reject Claim"
        else:
            rule_trace.append({"rule": "Checking Fraud Indicators", "result": facts.get('fraud_suspected')})
            if facts.get('fraud_suspected'):
                matched_rule = "IF fraud_suspected THEN Reject Claim"
            else:
                rule_trace.append({"rule": "Checking Verification Status", "result": facts.get('verification_pending')})
                if facts.get('verification_pending'):
                    matched_rule = "IF verification_pending THEN Manual Review Required"
                else:
                    rule_trace.append({"rule": "Verifying Core Requirements (Active, Documents, Report)", "result": facts.get('policy_active') and facts.get('documents_valid') and facts.get('incident_reported')})
                    if facts.get('policy_active') and facts.get('documents_valid') and facts.get('incident_reported'):
                        matched_rule = "IF policy_active AND documents_valid AND incident_reported THEN Approve Claim"
                    else:
                        matched_rule = "IF conditions incomplete THEN Manual Review Required"

        # 3. Confidence Breakdown panel data
        contributions = []
        if facts.get('policy_active'): contributions.append({"label": "Policy Active", "value": 30, "type": "positive"})
        else: contributions.append({"label": "Policy Inactive", "value": -50, "type": "negative"})

        if facts.get('documents_valid'): contributions.append({"label": "Documents Verified", "value": 30, "type": "positive"})
        else: contributions.append({"label": "Missing Documents", "value": -20, "type": "negative"})

        if facts.get('incident_reported'): contributions.append({"label": "Incident Reported", "value": 40, "type": "positive"})
        else: contributions.append({"label": "No Official Report", "value": -30, "type": "negative"})

        if facts.get('fraud_suspected'): contributions.append({"label": "Fraud Suspected", "value": -70, "type": "negative"})
        if facts.get('policy_expired'): contributions.append({"label": "Policy Expired", "value": -80, "type": "negative"})

        # 4. Reliability Analysis
        activated_rules = []
        inactive_rules = ["Fraud Rule", "Policy Expiry Rule", "Verification Rule", "Eligibility Rule"]
        
        # Determine which rule was activated
        if "policy_active" in matched_rule: 
            activated_rules.append("Eligibility Rule")
            inactive_rules.remove("Eligibility Rule")
        elif "fraud" in matched_rule: 
            activated_rules.append("Fraud Rule")
            inactive_rules.remove("Fraud Rule")
        elif "expired" in matched_rule: 
            activated_rules.append("Policy Expiry Rule")
            inactive_rules.remove("Policy Expiry Rule")
        elif "pending" in matched_rule: 
            activated_rules.append("Verification Rule")
            inactive_rules.remove("Verification Rule")

        reliability_level = "HIGH" if decision in ["Approved", "Rejected"] else "MEDIUM"
        if facts.get('fraud_suspected') or facts.get('verification_pending'):
            reliability_level = "MEDIUM"

        # 4. Priority Analysis (Conflict Resolution)
        priority_analysis = {
            "highest": "Fraud Detection Rule",
            "secondary": "Policy Eligibility Rule",
            "selected": "Fraud Detection Rule" if facts.get('fraud_suspected') or facts.get('policy_expired') else "Policy Eligibility Rule"
        }

        return {
            "facts": facts_display,
            "rule_trace": rule_trace,
            "matched_rule": matched_rule,
            "decision": decision,
            "contributions": contributions,
            "priority_analysis": priority_analysis,
            "activated_rules": activated_rules,
            "inactive_rules": inactive_rules,
            "reliability_level": reliability_level
        }
