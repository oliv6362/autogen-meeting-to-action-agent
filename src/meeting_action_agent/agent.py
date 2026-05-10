from autogen import ConversableAgent

from src.meeting_action_agent.config import LLM_CONFIG
from src.meeting_action_agent.tools.input_tool import read_meeting_file
from src.meeting_action_agent.tools.validation_tool import validate_meeting_output
from src.meeting_action_agent.tools.formatter_tool import format_meeting_report


def create_meeting_agent() -> ConversableAgent:
    meeting_agent = ConversableAgent(
        name="meeting_action_agent",
        system_message=(
            "You are an AI meeting-to-action assistant. "
            "Your task is to analyze meeting transcripts, notes, or messy project discussions "
            "and turn them into structured follow-up work. "
            "\n\n"
            "You must identify decisions, action items, owners, deadlines, open questions, and risks. "
            "\n\n"
            "You have access to these tools: "
            "read_meeting_file, validate_meeting_output, and format_meeting_report. "
            "\n\n"
            "Use read_meeting_file when the user provides a file path. "
            "If read_meeting_file returns success=false, do not continue with extraction. "
            "Report the error clearly and end with TERMINATE. "
            "After reading the meeting text, extract structured meeting information. "
            "After extracting structured information, use validate_meeting_output to check the result. "
            "If validation returns errors, correct the structured output once and validate it again. "
            "\n\n"
            "Rules: "
            "Do not invent information. "
            "Every decision, action item, open question, and risk must include evidence from the meeting text. "
            "Mark information as explicit only when it is clearly stated in the meeting text. "
            "Mark information as inferred when it is a reasonable conclusion but not directly stated. "
            "If an owner is missing, use 'Unclear'. "
            "If a deadline is missing, use 'Not specified'. "
            "If the meeting contains contradictions, mark them as unresolved instead of choosing one side. "
            "\n\n"
            "When the task is complete, end your response with TERMINATE."
        ),
        llm_config=LLM_CONFIG,
    )

    return meeting_agent


def create_user_proxy() -> ConversableAgent:
    user_proxy = ConversableAgent(
        name="user_proxy",
        llm_config=False,
        is_termination_msg=lambda msg: (
            msg.get("content") is not None and "TERMINATE" in msg["content"]
        ),
        human_input_mode="NEVER",
    )

    return user_proxy


def register_tools(meeting_agent: ConversableAgent, user_proxy: ConversableAgent) -> None:
    """
    Register Python functions as AutoGen tools.

    The meeting agent can request tools.
    The user proxy executes the actual Python functions.
    """

    meeting_agent.register_for_llm(
        name="read_meeting_file",
        description=(
            "Read a local meeting transcript or notes file. "
            "Input: file_path. "
            "Output: a dictionary with success, file_path, content, and error. "
            "If success is false, do not continue with extraction. "
            "Use this when the user provides a file path instead of directly providing meeting text."
        ),
    )(read_meeting_file)

    user_proxy.register_for_execution(
        name="read_meeting_file"
    )(read_meeting_file)

    meeting_agent.register_for_llm(
        name="validate_meeting_output",
        description=(
            "Validate structured meeting extraction output using deterministic Python checks. "
            "Input: structured meeting data as JSON-compatible data. "
            "Output: validation result with valid, errors, and warnings. "
            "Use this after extracting decisions, action items, open questions, and risks."
        ),
    )(validate_meeting_output)

    user_proxy.register_for_execution(
        name="validate_meeting_output"
    )(validate_meeting_output)