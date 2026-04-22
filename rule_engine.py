class RuleEngine:
    """
    Implements Propositional Logic using Forward Chaining Inference.
    """
    @staticmethod
    def evaluate(facts):
        # Decision logic based on forward chaining
        # facts: dictionary of boolean values
        
        # IF policy_expired OR fraud_suspected -> REJECTED
        if facts.get('policy_expired') or facts.get('fraud_suspected'):
            return "Rejected"
            
        # IF verification_pending -> MANUAL REVIEW
        if facts.get('verification_pending'):
            return "Manual Review Required"
            
        # IF policy_active AND documents_valid AND incident_reported -> APPROVED
        if facts.get('policy_active') and facts.get('documents_valid') and facts.get('incident_reported'):
            return "Approved"
            
        # Default fallback
        return "Manual Review Required"
