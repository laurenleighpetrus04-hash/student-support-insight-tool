# Bug Log

| Bug ID | Issue | Cause | Fix | Status |
|---|---|---|---|---|
| B001 | App failed when the synthetic dataset was missing | The app expected `data/synthetic_learners.csv` to already exist | Added a clear error message telling the user to run `python scripts/create_sample_data.py` | Fixed |
| B002 | Duplicate learner IDs were not detected | Duplicate validation was missing | Added duplicate checking using `df["learner_id"].duplicated()` | Fixed |
| B003 | Invalid confidence scores were accepted | No score range validation existed | Added validation to check that confidence scores are numeric and between 1 and 5 | Fixed |

## Refactoring Evidence

The prototype separates work into focused functions such as `load_data`, `validate_data`, `clean_data`, `calculate_risk_score`, `generate_insights`, and `generate_recommendations`. This keeps the MVP understandable and easier to test.
