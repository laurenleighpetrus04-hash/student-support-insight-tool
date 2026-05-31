# Bug Log

| Bug ID | Issue | Cause | Fix | Status |
|---|---|---|---|---|
| B001 | App failed when synthetic dataset was missing | The app expected the CSV file to already exist | Added clear error message telling user to run the data script | Fixed |
| B002 | Duplicate learner IDs were not detected | Duplicate validation was missing | Added duplicate check on learner_id | Fixed |
| B003 | Invalid confidence scores were accepted | No range validation existed | Added validation for scores from 1 to 5 | Fixed |