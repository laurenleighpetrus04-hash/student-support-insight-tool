# Test Log

| Test ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| T001 | Run app with default synthetic dataset | App opens and displays learner data | App opened successfully | Pass |
| T002 | Upload a valid CSV file | CSV uploads and dashboard updates | CSV uploaded and dashboard updated | Pass |
| T003 | Remove a required column from the CSV | App displays a validation error | Validation error displayed | Pass |
| T004 | Add a duplicate learner ID | App displays a duplicate learner ID warning | Duplicate warning displayed | Pass |
| T005 | Add a confidence score outside 1 to 5 | App displays an invalid score warning | Invalid score warning displayed | Pass |
| T006 | View dashboard visualisations | At least three visualisations display | Four visualisations displayed | Pass |
| T007 | View learners needing support | High and medium risk learners appear in a table | Support table displayed | Pass |
| T008 | Download summary report | TXT summary downloads successfully | TXT summary downloaded | Pass |
| T009 | Download cleaned dataset | Cleaned CSV downloads successfully | CSV downloaded | Pass |

## Notes

Testing focused on the MVP requirements: data input, validation, dashboard visualisations, support-risk logic, recommendations, privacy notice, and export.
