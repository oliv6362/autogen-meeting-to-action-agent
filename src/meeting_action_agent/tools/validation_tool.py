from typing import Any
from pydantic import ValidationError

from src.meeting_action_agent.models import MeetingExtraction, ValidationResult
from src.meeting_action_agent.logger import log_tool


@log_tool("validate_meeting_output")
def validate_meeting_output(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate structured meeting extraction output.

    This tool performs deterministic validation. It checks that the extracted
    meeting data follows the expected Pydantic schema and applies additional
    project-specific validation rules.

    Args:
        data: JSON-compatible dictionary containing extracted meeting information.

    Returns:
        A dictionary containing:
        - valid: Whether the output passed validation
        - errors: Blocking validation errors
        - warnings: Non-blocking quality issues
    """

    errors: list[str] = []
    warnings: list[str] = []

    try:
        meeting = MeetingExtraction.model_validate(data)
    except ValidationError as error:
        return ValidationResult(
            valid=False,
            errors=[str(error)],
            warnings=[],
        ).model_dump()

    _validate_summary(meeting, warnings)
    _validate_decisions(meeting, errors, warnings)
    _validate_action_items(meeting, errors, warnings)
    _validate_open_questions(meeting, errors, warnings)
    _validate_risks(meeting, errors, warnings)

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    ).model_dump()


def _validate_summary(meeting: MeetingExtraction, warnings: list[str]) -> None:
    if not meeting.summary.strip():
        warnings.append("Meeting summary is empty.")


def _validate_decisions(meeting: MeetingExtraction, errors: list[str], warnings: list[str]) -> None:
    for index, decision in enumerate(meeting.decisions, start=1):
        if not decision.decision.strip():
            errors.append(f"Decision {index} is missing decision text.")

        if not decision.evidence:
            warnings.append(f"Decision {index} has no supporting evidence.")

        if decision.status in {"inferred", "unclear"}:
            warnings.append(f"Decision {index} has status '{decision.status}' and should be reviewed.")


def _validate_action_items(meeting: MeetingExtraction, errors: list[str], warnings: list[str]) -> None:
    for index, action_item in enumerate(meeting.action_items, start=1):
        if not action_item.task.strip():
            errors.append(f"Action item {index} is missing task text.")

        if not action_item.owner.strip():
            errors.append(f"Action item {index} is missing an owner field.")
        elif action_item.owner.lower() == "unclear":
            warnings.append(f"Action item {index} has an unclear owner.")

        if not action_item.deadline.strip():
            errors.append(f"Action item {index} is missing a deadline field.")
        elif action_item.deadline.lower() == "not specified":
            warnings.append(f"Action item {index} has no specified deadline.")

        if not action_item.context.strip():
            warnings.append(f"Action item {index} has no context.")

        if not action_item.evidence:
            warnings.append(f"Action item {index} has no supporting evidence.")

        if action_item.status in {"inferred", "unclear"}:
            warnings.append(f"Action item {index} has status '{action_item.status}' and should be reviewed.")


def _validate_open_questions(meeting: MeetingExtraction, errors: list[str], warnings: list[str]) -> None:
    for index, open_question in enumerate(meeting.open_questions, start=1):
        if not open_question.question.strip():
            errors.append(f"Open question {index} is missing question text.")

        if not open_question.evidence:
            warnings.append(f"Open question {index} has no supporting evidence.")

        if open_question.status in {"inferred", "unclear"}:
            warnings.append(f"Open question {index} has status '{open_question.status}' and should be reviewed.")


def _validate_risks(meeting: MeetingExtraction, errors: list[str], warnings: list[str]) -> None:
    for index, risk in enumerate(meeting.risks, start=1):
        if not risk.risk.strip():
            errors.append(f"Risk {index} is missing risk text.")

        if not risk.evidence:
            warnings.append(f"Risk {index} has no supporting evidence.")

        if risk.status in {"inferred", "unclear"}:
            warnings.append(f"Risk {index} has status '{risk.status}' and should be reviewed.")