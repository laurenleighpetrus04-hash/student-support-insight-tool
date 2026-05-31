
---

### `evidence/test_log.md`

```markdown
# Test Log

| Test ID | Test Case | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| T001 | Run app with default dataset | App opens and displays data | App opened successfully | Pass |
| T002 | Upload valid CSV | Dashboard updates | Dashboard updated | Pass |
| T003 | Remove required column | Validation error appears | Error appeared | Pass |
| T004 | Duplicate learner ID | Warning appears | Warning appeared | Pass |
| T005 | Confidence score outside 1 to 5 | Warning appears | Warning appeared | Pass |
| T006 | View charts | At least 3 charts display | 4 charts displayed | Pass |
| T007 | Download summary report | TXT file downloads | TXT downloaded | Pass |
| T008 | Download cleaned dataset | CSV file downloads | CSV downloaded | Pass |