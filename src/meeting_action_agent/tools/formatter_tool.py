from typing import Any

from src.meeting_action_agent.models import EvidenceItem, MeetingExtraction
from src.meeting_action_agent.logger import log_tool


@log_tool("format_meeting_report")
def format_meeting_report(data: dict[str, Any]) -> str:
    """
    Format structured meeting extraction data as a Markdown report.

    Args:
        data: JSON-compatible dictionary containing extracted meeting information.

    Returns:
        A Markdown-formatted meeting follow-up report.
    """

    meeting = MeetingExtraction.model_validate(data)

    sections = [
        f"# {meeting.meeting_title}",
        "",
        "## Summary",
        meeting.summary,
        "",
        "## Decisions",
        _format_decisions_table(meeting),
        "",
        "## Action Items",
        _format_action_items_table(meeting),
        "",
        "## Open Questions",
        _format_open_questions_table(meeting),
        "",
        "## Risks",
        _format_risks_table(meeting),
    ]

    return "\n".join(sections).strip()


def _format_decisions_table(meeting: MeetingExtraction) -> str:
    if not meeting.decisions:
        return "No decisions identified."

    lines = [
        "| Decision | Status | Evidence |",
        "|---|---|---|",
    ]

    for decision in meeting.decisions:
        lines.append(
            "| "
            f"{_escape_table_text(decision.decision)} | "
            f"{_escape_table_text(decision.status)} | "
            f"{_escape_table_text(_format_evidence(decision.evidence))} |"
        )

    return "\n".join(lines)


def _format_action_items_table(meeting: MeetingExtraction) -> str:
    if not meeting.action_items:
        return "No action items identified."

    lines = [
        "| Task | Owner | Deadline | Status | Context | Evidence |",
        "|---|---|---|---|---|---|",
    ]

    for action_item in meeting.action_items:
        lines.append(
            "| "
            f"{_escape_table_text(action_item.task)} | "
            f"{_escape_table_text(action_item.owner)} | "
            f"{_escape_table_text(action_item.deadline)} | "
            f"{_escape_table_text(action_item.status)} | "
            f"{_escape_table_text(action_item.context)} | "
            f"{_escape_table_text(_format_evidence(action_item.evidence))} |"
        )

    return "\n".join(lines)


def _format_open_questions_table(meeting: MeetingExtraction) -> str:
    if not meeting.open_questions:
        return "No open questions identified."

    lines = [
        "| Question | Status | Evidence |",
        "|---|---|---|",
    ]

    for open_question in meeting.open_questions:
        lines.append(
            "| "
            f"{_escape_table_text(open_question.question)} | "
            f"{_escape_table_text(open_question.status)} | "
            f"{_escape_table_text(_format_evidence(open_question.evidence))} |"
        )

    return "\n".join(lines)


def _format_risks_table(meeting: MeetingExtraction) -> str:
    if not meeting.risks:
        return "No risks identified."

    lines = [
        "| Risk | Status | Evidence |",
        "|---|---|---|",
    ]

    for risk in meeting.risks:
        lines.append(
            "| "
            f"{_escape_table_text(risk.risk)} | "
            f"{_escape_table_text(risk.status)} | "
            f"{_escape_table_text(_format_evidence(risk.evidence))} |"
        )

    return "\n".join(lines)


def _format_evidence(evidence_items: list[EvidenceItem]) -> str:
    if not evidence_items:
        return "No evidence provided"

    quotes = [f'"{item.quote}"' for item in evidence_items if item.quote.strip()]

    if not quotes:
        return "No evidence provided"

    return "; ".join(quotes)


def _escape_table_text(value: str) -> str:
    """
    Escape text so it is safe to place inside a Markdown table cell.
    """

    return value.replace("|", "\\|").replace("\n", " ").strip()