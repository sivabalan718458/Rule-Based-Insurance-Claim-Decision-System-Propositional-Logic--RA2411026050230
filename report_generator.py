import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

class ReportGenerator:
    @staticmethod
    def generate_pdf(claim, user, xai, file_path):
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        margin = 1*inch
        y = height - margin

        def draw_section_title(title, y_pos):
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.HexColor("#3b82f6")) # Blue section titles
            c.drawString(margin, y_pos, title)
            c.setFillColor(colors.black)
            return y_pos - 0.3*inch

        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2.0, y, "INSURANCE CLAIM DECISION REPORT")
        y -= 0.3*inch
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2.0, y, "Rule-Based Inference using Propositional Logic")
        y -= 0.7*inch

        # SECTION 1: INPUT FACT BASE
        y = draw_section_title("SECTION 1: INPUT FACT BASE", y)
        c.setFont("Helvetica", 11)
        facts_map = {
            "Policy Active": claim.policy_active,
            "Documents Valid": claim.documents_valid,
            "Incident Reported": claim.incident_reported,
            "Policy Expired": claim.policy_expired,
            "Verification Pending": claim.verification_pending,
            "Fraud Suspected": claim.fraud_suspected
        }
        for label, val in facts_map.items():
            c.drawString(margin + 0.2*inch, y, f"{label}: {'TRUE' if val else 'FALSE'}")
            y -= 0.2*inch
        y -= 0.3*inch

        # SECTION 2: FORWARD CHAINING EXECUTION TRACE
        y = draw_section_title("SECTION 2: FORWARD CHAINING EXECUTION TRACE", y)
        c.setFont("Helvetica", 11)
        for step in xai['rule_trace']:
            c.drawString(margin + 0.2*inch, y, f"{step['rule']} -> {'TRUE' if step['result'] else 'FALSE'}")
            y -= 0.2*inch
        y -= 0.3*inch

        # SECTION 3: MATCHED RULE APPLIED
        y = draw_section_title("SECTION 3: MATCHED RULE APPLIED", y)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin + 0.2*inch, y, xai['matched_rule'])
        y -= 0.6*inch

        # SECTION 4: FINAL DECISION
        y = draw_section_title("SECTION 4: FINAL DECISION", y)
        c.setFont("Helvetica-Bold", 20)
        decision_text = f"CLAIM {claim.decision.upper()}"
        if "Manual" in claim.decision:
            decision_text = "MANUAL REVIEW REQUIRED"
        
        c.drawCentredString(width/2.0, y - 0.2*inch, decision_text)
        
        # Footer
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(colors.grey)
        footer = "Generated using Rule-Based Expert System with Propositional Logic and Forward Chaining Inference"
        c.drawCentredString(width/2.0, 0.5*inch, footer)

        c.save()
        return file_path
