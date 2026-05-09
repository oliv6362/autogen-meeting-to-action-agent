from autogen import ConversableAgent

from src.meeting_action_agent.config import LLM_CONFIG
from src.meeting_action_agent.tools.input_tool import read_meeting_file


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