# Final Report Outline

## 1. Cover Page

Project: Student Support Insights Tool  
Intern Name: Lauren Leigh Petrus
Programme: AI Internship  
Date: 05/31/2026

## 2. Executive Summary

This project developed an MVP prototype that helps programme staff analyse learner support survey data. The tool validates data, visualises support needs, flags learners who may need support, and generates practical recommendations.

## 3. Problem Statement and Context

Digital skills programmes collect learner information, but this data is not always used systematically. This tool helps staff use learner data responsibly to identify support needs and improve learner success.

## 4. Stakeholder and User Needs

Stakeholders include learners, programme staff, tutors, mentors, and programme managers.

## 5. Current and Improved Process

Refer to:

- evidence/as_is_process.md
- evidence/to_be_process.md

## 6. Business / Value Model

Refer to:

- evidence/value_model.md

## 7. Data Description and Preparation

The dataset contains 50 synthetic learner records. No real personal data was used.

Validation checks include:

- Missing values
- Duplicate learner IDs
- Invalid confidence scores
- Invalid category values

## 8. Analytics Findings and Visualisations

The dashboard includes:

1. Learners by support need
2. Internet access distribution
3. Average confidence scores
4. Support risk level distribution

## 9. Prototype Description

The prototype was built using Python, Streamlit, pandas, and Plotly.

## 10. AI, Data Ethics and Privacy Review

The tool uses rule-based logic and does not make final decisions about learners. It should only support human decision-making.

Privacy principles:

- Use synthetic or anonymised data
- Collect consent for real learner data
- Store learner data securely
- Avoid unfair profiling
- Require human review

The tool should not be used to reject, punish, or exclude learners.

## 11. Methods, Tools and Development Approach

Tools used:

| Tool | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | App interface |
| pandas | Data cleaning and analysis |
| Plotly | Charts |
| GitHub Codespaces | Development environment |
| Markdown | Documentation |

## 12. Testing and Review Evidence

Refer to:

- evidence/test_log.md
- evidence/bug_log.md
- evidence/screenshots/

## 13. Reflection

The MVP shows how learner survey data can be turned into useful support insights. The main challenge was keeping the scope small while still meeting the requirements.

## 14. Evidence Inventory

| Requirement | Evidence |
|---|---|
| Working prototype | app.py |
| Dataset | data/synthetic_learners.csv |
| Data dictionary | data/data_dictionary.md |
| Visualisations | Dashboard screenshots |
| Insights | App output |
| Recommendations | App output |
| Ethics review | Final report section |
| Process diagrams | evidence/as_is_process.md and evidence/to_be_process.md |
| Value model | evidence/value_model.md |
| Testing log | evidence/test_log.md |
| Bug log | evidence/bug_log.md |