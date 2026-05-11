# Data Import Planning

## Summary
The team discussed the plan to import old customer records into the new CRM, focusing on normalizing column names and limiting the initial scope to active customers with available email addresses.

## Decisions
| Decision | Status | Evidence |
|---|---|---|
| The first import will include only active customers. | explicit | "We decided that the first import will include only active customers." |
| The import script should skip records without email addresses for now. | explicit | "Then the import script should skip records without email addresses for now." |

## Action Items
| Task | Owner | Deadline | Status | Context | Evidence |
|---|---|---|---|---|---|
| Write a mapping script that normalizes the column names before import. | Oliver | Friday | explicit | To handle old CSV files with different column names depending on the exporting department. | "I can write a mapping script that normalizes the column names before import. I can finish that by Friday." |
| Prepare a sample CSV file for testing. | Daniel | Wednesday | explicit | For testing the data import process. | "I can prepare a sample CSV file for testing by Wednesday." |

## Open Questions
| Question | Status | Evidence |
|---|---|---|
| Whether archived customers should be imported later. | explicit | "We still need to decide whether archived customers should be imported later." |

## Risks
| Risk | Status | Evidence |
|---|---|---|
| Old CSV files have different column names depending on which department exported them. | explicit | "The old CSV files have different column names depending on which department exported them." |
| Some records may also be missing email addresses. | explicit | "Some records may also be missing email addresses." |