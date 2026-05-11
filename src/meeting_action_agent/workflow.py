import json
from pathlib import Path
from typing import Any

from src.meeting_action_agent.agent import create_agents
from src.meeting_action_agent.config import DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_FILE
from src.meeting_action_agent.tools.formatter_tool import format_meeting_report
from src.meeting_action_agent.tools.validation_tool import validate_meeting_output


def run_meeting_workflow(input_file: str = DEFAULT_INPUT_FILE, output_file: str = DEFAULT_OUTPUT_FILE) -> str:
    """
    Run the Meeting-to-Action Agent workflow.

    The workflow:
    1. Lets the AutoGen agent call the read_meeting_file tool.
    2. Uses the LLM agent to extract structured meeting information.
    3. Validates the structured output using a deterministic validation tool.
    4. Formats the validated result as a Markdown report using a deterministic formatter tool.
    5. Saves the final result.

    Args:
        input_file: Path to the meeting transcript or notes file.
        output_file: Path where the final Markdown report should be saved.

    Returns:
        The final Markdown report or a validation/error report.
    """

    meeting_agent, user_proxy = create_agents()

    extraction_prompt = _build_extraction_prompt(input_file)

    chat_result = user_proxy.initiate_chat(
        meeting_agent,
        message=extraction_prompt,
        max_turns=4,
    )

    raw_response = chat_result.summary

    try:
        extracted_data = _extract_json_from_response(raw_response)
    except ValueError as error:
        cleaned_response = raw_response.replace("TERMINATE", "").strip()

        if not cleaned_response:
            error_message = "The LLM did not return a JSON object after reading the meeting file."
        else:
            error_message = f"{error}\n\nRaw response:\n{cleaned_response}"

        error_report = _build_error_report(error_message)
        _save_output(error_report, output_file)
        return error_report

    validation_result = validate_meeting_output(extracted_data)

    if not validation_result["valid"]:
        validation_report = _build_validation_report(validation_result)
        _save_output(validation_report, output_file)
        return validation_report

    final_report = format_meeting_report(extracted_data)

    if validation_result["warnings"]:
        final_report = _append_validation_warnings(
            report=final_report,
            warnings=validation_result["warnings"],
        )

    _save_output(final_report, output_file)

    return final_report


def _build_extraction_prompt(input_file: str) -> str:
    """
    Build the extraction prompt sent to the LLM agent.

    The LLM must call read_meeting_file to retrieve the meeting text. After that,
    it should return structured JSON only. Validation, formatting, and saving are
    handled by deterministic Python code in the workflow.
    """

    return (
        "Read and analyze the meeting transcript from this file path:\n"
        f"{input_file}\n\n"
        "Required steps:\n"
        "1. Use the read_meeting_file tool to read the file.\n"
        "2. If read_meeting_file returns success=false, report the error and end with TERMINATE.\n"
        "3. If read_meeting_file returns success=true, use the content field as the meeting text.\n"
        "4. Extract structured follow-up information from the meeting text.\n"
        "5. Return one valid JSON object only.\n"
        "6. After the JSON object, write TERMINATE on a separate line.\n\n"
        "Do not return Markdown. Do not explain the result.\n"
        "Do not include TERMINATE inside the JSON object.\n\n"
        "The JSON must follow this exact nested schema:\n"
        "{\n"
        '  "meeting_title": "Short meeting title",\n'
        '  "summary": "Brief summary of the meeting",\n'
        '  "decisions": [\n'
        "    {\n"
        '      "decision": "Decision text",\n'
        '      "status": "explicit",\n'
        '      "evidence": [\n'
        '        {"quote": "Supporting quote from the meeting text"}\n'
        "      ]\n"
        "    }\n"
        "  ],\n"
        '  "action_items": [\n'
        "    {\n"
        '      "task": "Task text",\n'
        '      "owner": "Owner name or Unclear",\n'
        '      "deadline": "Deadline or Not specified",\n'
        '      "context": "Why this task exists",\n'
        '      "status": "explicit",\n'
        '      "evidence": [\n'
        '        {"quote": "Supporting quote from the meeting text"}\n'
        "      ]\n"
        "    }\n"
        "  ],\n"
        '  "open_questions": [\n'
        "    {\n"
        '      "question": "Open question text",\n'
        '      "status": "explicit",\n'
        '      "evidence": [\n'
        '        {"quote": "Supporting quote from the meeting text"}\n'
        "      ]\n"
        "    }\n"
        "  ],\n"
        '  "risks": [\n'
        "    {\n"
        '      "risk": "Risk text",\n'
        '      "status": "explicit",\n'
        '      "evidence": [\n'
        '        {"quote": "Supporting quote from the meeting text"}\n'
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Schema rules:\n"
        "- Use decision, not description, for decisions.\n"
        "- Use task, not description or action_item, for action items.\n"
        "- Use question, not description or open_question, for open questions.\n"
        "- Use risk, not description, for risks.\n"
        "- Use status on every decision, action item, open question, and risk.\n"
        "- Status values must be exactly: explicit, inferred, unclear.\n"
        "- Evidence must always be a list of objects with a quote field.\n"
        "- Do not create fields such as topic, description, assigned_to, due_date, actions, key_decisions, rationale, stakeholders, likelihood, or impact.\n"
        "- If an owner is missing, use Unclear.\n"
        "- If a deadline is missing, use Not specified.\n"
        "- Do not include a question as an open question if it is answered later in the transcript.\n"
        "- If a question is answered with an agreement or decision, include it as a decision instead of an open question.\n"
        "- Every decision, action item, open question, and risk must include evidence from the meeting text.\n"
    )


def _extract_json_from_response(response: str) -> dict[str, Any]:
    """
    Extract and parse JSON from the LLM response.

    The ideal response is pure JSON, but this function also handles cases where
    the model wraps the JSON in a Markdown code block or appends TERMINATE.
    """

    cleaned_response = response.replace("TERMINATE", "").strip()

    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response.removeprefix("```json").strip()

    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.removeprefix("```").strip()

    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response.removesuffix("```").strip()

    start_index = cleaned_response.find("{")
    end_index = cleaned_response.rfind("}")

    if start_index == -1 or end_index == -1:
        raise ValueError("The LLM response did not contain a JSON object.")

    json_text = cleaned_response[start_index:end_index + 1]

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as error:
        raise ValueError(f"The LLM response could not be parsed as JSON: {error}") from error

    if not isinstance(parsed, dict):
        raise ValueError("The parsed LLM response was not a JSON object.")

    return parsed


def _build_error_report(error_message: str) -> str:
    """
    Build a Markdown error report.
    """

    return (
        "# Meeting-to-Action Agent Error\n\n"
        "The workflow could not complete successfully.\n\n"
        f"## Error\n{error_message}"
    )


def _build_validation_report(validation_result: dict[str, Any]) -> str:
    """
    Build a Markdown report for validation failures.
    """

    lines = [
        "# Meeting-to-Action Validation Failed",
        "",
        "The LLM extracted meeting data, but the result did not pass deterministic validation.",
        "",
        "## Errors",
    ]

    errors = validation_result.get("errors", [])

    if errors:
        for error in errors:
            lines.append(f"- {error}")
    else:
        lines.append("- No validation errors reported.")

    warnings = validation_result.get("warnings", [])

    if warnings:
        lines.append("")
        lines.append("## Warnings")
        for warning in warnings:
            lines.append(f"- {warning}")

    return "\n".join(lines)


def _append_validation_warnings(report: str, warnings: list[str]) -> str:
    """
    Append non-blocking validation warnings to the final Markdown report.
    """

    if not warnings:
        return report

    lines = [
        report,
        "",
        "## Validation Warnings",
    ]

    for warning in warnings:
        lines.append(f"- {warning}")

    return "\n".join(lines)


def _save_output(content: str, output_file: str) -> None:
    """
    Save workflow output to a Markdown file.
    """

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content.strip(), encoding="utf-8")