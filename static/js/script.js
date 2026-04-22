document.addEventListener('DOMContentLoaded', () => {
    // Tab switching logic
    const navLinks = document.querySelectorAll('.nav-link');
    const tabContents = document.querySelectorAll('.tab-content');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            if (link.classList.contains('logout-btn')) return;
            
            e.preventDefault();
            const tabId = link.getAttribute('data-tab');

            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tabId) {
                    content.classList.add('active');
                }
            });
        });
    });

    // Handle claim evaluation form
    const assessmentForm = document.getElementById('assessment-form');
    if (assessmentForm) {
        assessmentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(assessmentForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/evaluate_claim', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                if (result.success) {
                    renderXAIInsights(result.data);
                    // Switch to insights tab
                    document.querySelector('[data-tab="insights"]').click();
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Evaluation failed. Please try again.');
            }
        });
    }

    function renderXAIInsights(data) {
        const xai = data.explanation_data;

        // 1. Decision Header Panel
        const header = document.getElementById('decision-header');
        const headerText = document.getElementById('decision-text-header');
        headerText.innerText = data.decision.toUpperCase();
        header.className = 'decision-header-panel ' + (
            data.decision === 'Approved' ? 'decision-header-approved' : 
            data.decision === 'Rejected' ? 'decision-header-rejected' : 'decision-header-review'
        );

        // 2. Fact Base
        const factGrid = document.getElementById('fact-base-grid');
        factGrid.innerHTML = '';
        Object.entries(xai.facts).forEach(([label, value]) => {
            const item = document.createElement('div');
            item.className = 'fact-item';
            item.innerHTML = `
                <span>${label}</span>
                <span class="badge ${value ? 'badge-success' : 'badge-danger'}">${value ? 'TRUE' : 'FALSE'}</span>
            `;
            factGrid.appendChild(item);
        });

        // 3. Timeline (UPGRADE 1)
        const timeline = document.getElementById('timeline-container');
        timeline.innerHTML = '';
        xai.rule_trace.forEach((step, index) => {
            const card = document.createElement('div');
            card.className = 'timeline-step';
            card.innerHTML = `
                <div class="timeline-marker"></div>
                <div class="timeline-step-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-weight: 800; font-size: 0.75rem; color: var(--primary); text-transform: uppercase;">Step ${index + 1}</span>
                        <span class="badge ${step.result ? 'badge-true' : 'badge-false'}">${step.result ? 'MATCH' : 'SKIP'}</span>
                    </div>
                    <div style="font-weight: 600; font-size: 1rem;">${step.rule}</div>
                    <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.3rem;">
                        Evaluation Result: <strong>${step.result ? 'TRUE' : 'FALSE'}</strong>
                    </div>
                </div>
            `;
            timeline.appendChild(card);
        });

        // 4. Matched Rule (UPGRADE 2)
        const ruleParts = xai.matched_rule.split(' THEN ');
        document.getElementById('rule-condition').innerText = ruleParts[0].replace('IF ', '');
        const ruleDecision = document.getElementById('rule-decision');
        ruleDecision.innerText = ruleParts[1];
        ruleDecision.className = 'rule-decision-box ' + (
            data.decision === 'Approved' ? 'decision-approved' : 
            data.decision === 'Rejected' ? 'decision-rejected' : 'decision-review'
        );

        // 5. Priority Analysis (UPGRADE 3)
        document.getElementById('selected-priority').innerText = xai.priority_analysis.selected;

        // 6. Risk & Confidence
        const riskBadge = document.getElementById('risk-badge-large');
        if (riskBadge) {
            riskBadge.innerText = data.risk_level;
            riskBadge.className = 'badge ' + (
                data.risk_level === 'LOW RISK' ? 'badge-success' : 
                data.risk_level === 'MEDIUM RISK' ? 'badge-warning' : 'badge-danger'
            );
        }

        const confText = document.getElementById('confidence-text-large');
        if (confText) confText.innerText = data.confidence_score + '%';
        
        const confFill = document.getElementById('confidence-progress-fill');
        if (confFill) {
            setTimeout(() => {
                confFill.style.width = data.confidence_score + '%';
            }, 100);
        }

        // 7. Confidence Breakdown
        const breakdown = document.getElementById('confidence-breakdown-container');
        if (breakdown) {
            breakdown.innerHTML = '';
            xai.contributions.forEach(contrib => {
                const row = document.createElement('div');
                row.className = 'contribution-bar';
                const absVal = Math.abs(contrib.value);
                row.innerHTML = `
                    <div class="contrib-label">${contrib.label}</div>
                    <div class="contrib-progress progress-container" style="height: 8px;">
                        <div class="progress-fill" style="width: ${absVal}%; background: ${contrib.type === 'positive' ? 'var(--success)' : 'var(--danger)'};"></div>
                    </div>
                    <div class="contrib-value" style="color: ${contrib.type === 'positive' ? 'var(--success)' : 'var(--danger)'}">
                        ${contrib.type === 'positive' ? '+' : '-'}${absVal}%
                    </div>
                `;
                breakdown.appendChild(row);
            });
        }

        // 7. Reliability Analysis (FEATURE 1)
        const relBadge = document.getElementById('reliability-level-badge');
        relBadge.innerText = xai.reliability_level;
        relBadge.className = 'badge ' + (
            xai.reliability_level === 'HIGH' ? 'reliability-high' : 
            xai.reliability_level === 'MEDIUM' ? 'reliability-medium' : 'reliability-low'
        );

        const activeContainer = document.getElementById('activated-rules-container');
        const inactiveContainer = document.getElementById('inactive-rules-container');
        activeContainer.innerHTML = '';
        inactiveContainer.innerHTML = '';

        xai.activated_rules.forEach(rule => {
            const span = document.createElement('span');
            span.className = 'rule-active-badge';
            span.innerText = rule;
            activeContainer.appendChild(span);
        });

        xai.inactive_rules.forEach(rule => {
            const span = document.createElement('span');
            span.className = 'rule-inactive-badge';
            span.innerText = rule;
            inactiveContainer.appendChild(span);
        });

        // 8. Eligibility Score Meter
        const eligibilityText = document.getElementById('eligibility-text');
        const eligibilityFill = document.getElementById('eligibility-progress-fill');
        const eligibilityLabel = document.getElementById('eligibility-label');
        const score = data.eligibility_score;

        if (eligibilityText) {
            eligibilityText.innerText = score + '%';
            eligibilityFill.className = 'progress-fill ' + (
                score >= 80 ? 'bg-success' : score >= 50 ? 'bg-warning' : 'bg-danger'
            );
            eligibilityLabel.innerText = score >= 80 ? 'HIGH ELIGIBILITY' : score >= 50 ? 'MODERATE ELIGIBILITY' : 'LOW ELIGIBILITY';
            eligibilityLabel.style.color = score >= 80 ? 'var(--success)' : score >= 50 ? 'var(--warning)' : 'var(--danger)';

            setTimeout(() => {
                eligibilityFill.style.width = score + '%';
            }, 100);
        }

        // 9. Update History Table Dynamically
        updateHistoryTable(data);
    }

    function updateHistoryTable(data) {
        const historyBody = document.getElementById('claim-history-body');
        if (!historyBody) return;

        const newRow = document.createElement('tr');
        
        if (historyBody.children.length === 1 && historyBody.innerText.includes('No claims')) {
            historyBody.innerHTML = '';
        }

        newRow.innerHTML = `
            <td>${data.claim_type}</td>
            <td><span class="badge ${data.decision === 'Approved' ? 'badge-success' : data.decision === 'Rejected' ? 'badge-danger' : 'badge-warning'}">${data.decision}</span></td>
            <td><span class="badge ${data.risk_level === 'LOW RISK' ? 'badge-success' : data.risk_level === 'MEDIUM RISK' ? 'badge-warning' : 'badge-danger'}">${data.risk_level}</span></td>
            <td>${data.confidence_score}%</td>
            <td style="color: var(--text-muted); font-size: 0.85rem;">${data.timestamp}</td>
            <td style="display: flex; gap: 0.5rem;">
                <a href="/generate_report/${data.id}" class="btn-primary" style="padding: 0.4rem 0.8rem; font-size: 0.75rem; width: auto; border-radius: 8px; text-decoration: none;">Report</a>
                <a href="/delete_claim/${data.id}" class="btn-primary delete-btn" style="padding: 0.4rem 0.8rem; font-size: 0.75rem; width: auto; border-radius: 8px; text-decoration: none;">Delete</a>
            </td>
        `;
        
        historyBody.insertBefore(newRow, historyBody.firstChild);
        
        // Add listener to new delete button
        newRow.querySelector('.delete-btn').addEventListener('click', handleDelete);

        if (historyBody.children.length > 5) {
            historyBody.removeChild(historyBody.lastChild);
        }
    }

    // Confirmation logic for all delete buttons
    function handleDelete(e) {
        if (!confirm('Are you sure you want to delete this claim record? This action cannot be undone.')) {
            e.preventDefault();
        }
    }

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', handleDelete);
    });
});
