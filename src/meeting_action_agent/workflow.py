from pathlib import Path

from src.meeting_action_agent.agent import create_agents
from src.meeting_action_agent.config import DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_FILE


def run_meeting_workflow(input_file: str = DEFAULT_INPUT_FILE, output_file: str = DEFAULT_OUTPUT_FILE) -> str:
    """
    Run the Meeting-to-Action Agent workflow.

    The workflow asks the AutoGen meeting agent to:
    1. Read a meeting transcript file.
    2. Extract structured meeting follow-up information.
    3. Validate the structured output.

    Args:
        input_file: Path to the meeting transcript or notes file.
        output_file: Path where the final Markdown report should be saved.

    Returns:
        The final chat summary produced by AutoGen.
    """

    meeting_agent, user_proxy = create_agents()

    task_message = _build_task_message(input_file)

    chat_result = user_proxy.initiate_chat(
        meeting_agent,
        message=task_message,
        max_turns=10,
    )

    _save_chat_summary(chat_result.summary, output_file)

    return chat_result.summary


def _build_task_message(input_file: str) -> str:
    """
    Build the task instruction sent to the meeting agent.
    """

    return (
        "Analyze the meeting transcript from this file:\n"
        f"{input_file}\n\n"
        "Required workflow:\n"
        "1. Use read_meeting_file to read the file.\n"
        "2. If read_meeting_file returns success=false, report the error and stop.\n"
        "3. If read_meeting_file returns success=true, extract the meeting information into structured JSON-compatible data.\n"
        "4. Use validate_meeting_output to validate the structured data.\n"
        "5. If validation returns errors, correct the data once and validate again.\n"
        "The structured data must include these top-level fields:\n"
        "- meeting_title\n"
        "- summary\n"
        "- decisions\n"
        "- action_items\n"
        "- open_questions\n"
        "- risks\n\n"
        "Every decision, action item, open question, and risk must include evidence "
        "from the meeting text.\n\n"
        "When the task is complete, end your response with TERMINATE."
    )


def _save_chat_summary(summary: str, output_file: str) -> None:
    """
    Save the final AutoGen chat summary to a Markdown file.
    """

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cleaned_summary = summary.replace("TERMINATE", "").strip()

    output_path.write_text(cleaned_summary, encoding="utf-8")