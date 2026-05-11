# Evaluation Results

This file summarizes the evaluation of the Meeting-to-Action Agent on 10 fixed test cases.

The agent was evaluated on meeting transcripts covering clear planning meetings, missing owners, missing deadlines, unresolved questions, messy notes, customer interviews, and failure cases.

## Summary

| Case | Focus | Result | Notes |
|---|---|---|---|
| 01 | Clear sprint planning | Passed | Extracted decisions, action items, open questions, and risks. |
| 02 | Missing deadline | Mostly passed | Correctly handled missing deadline, but kept a resolved question as open. |
| 03 | Missing owner | Passed | Correctly used `Unclear` for missing owner. |
| 04 | No action items | Failed | The local model did not return a JSON object after reading the file. |
| 05 | Resolved question | Failed | The local model did not return a JSON object after reading the file. |
| 06 | Unresolved questions | Passed | Correctly extracted unresolved questions. |
| 07 | Data import / inferred risks | Mostly passed | Extracted useful output, but classified implied risks as explicit. |
| 08 | Conflicting scope discussion | Passed | Correctly handled unresolved scope. |
| 09 | Messy notes | Passed | Extracted structured output from bullet-style notes. |
| 10 | Customer interview | Mostly passed | Extracted useful follow-up work, but some decisions were too broadly interpreted. |

## Overall Result

The agent passed or mostly passed 8 out of 10 test cases.

The two failed cases are kept in the evaluation to document realistic limitations of the local LLM/tool-call workflow.

## Key Findings

The agent performs best when meeting decisions, action items, owners, deadlines, and risks are clearly stated.

The main weaknesses are:

- Inconsistent behavior after tool calls
- Difficulty handling cases with no action items
- Occasional confusion between resolved questions, open questions, and decisions
- Occasional over-classification of inferred risks as explicit risks

## Tool Call Logging

Tool calls are logged in `logs/tool_calls.jsonl`.

Each logged tool call includes:

- timestamp
- tool name
- input arguments
- tool output

Successful cases usually include calls to:

1. `read_meeting_file`
2. `validate_meeting_output`
3. `format_meeting_report`

Failed cases may only include `read_meeting_file` because the workflow stops if the LLM does not return a valid JSON object.

## Evaluation Files

- Test cases: `evaluation/test_cases/`
- Generated outputs: `evaluation/outputs/`
- Tool call log: `logs/tool_calls.jsonl`

