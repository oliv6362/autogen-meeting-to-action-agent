from autogen import ConversableAgent

from src.meeting_action_agent.config import LLM_CONFIG
from src.meeting_action_agent.tools.input_tool import read_meeting_file


def create_meeting_agent() -> ConversableAgent:
    """
    Create the LLM-powered meeting extraction agent.

    The agent is responsible for reading meeting text through the input tool
    and extracting structured data. Deterministic validation, formatting, and
    logging are handled by the workflow.
    """

    meeting_agent = ConversableAgent(
        name="meeting_action_agent",
        system_message=(
            "You are an AI meeting-to-action extraction assistant. "
            "Your task is to read meeting transcripts and extract structured follow-up information. "
            "You must identify decisions, action items, owners, deadlines, open questions, and risks. "
            "You may use the read_meeting_file tool when the workflow gives you a file path. "
            "Do not invent information. "
            "Every extracted decision, action item, open question, and risk must include evidence from the meeting text. "
            "Use explicit when information is directly stated. "
            "Use inferred when it is a reasonable conclusion but not directly stated. "
            "Use unclear when the information is ambiguous. "
            "If an owner is missing, use 'Unclear'. "
            "If a deadline is missing, use 'Not specified'. "
            "Return only the structured JSON data requested by the workflow. "
            "When the task is complete, write TERMINATE on a separate line. "
        ),
        llm_config=LLM_CONFIG,
    )

    return meeting_agent


def create_user_proxy() -> ConversableAgent:
    """
    Create the non-LLM user proxy agent.

    The user proxy executes registered tools. Human input is disabled so the
    workflow can run automatically during normal execution and evaluation.
    """

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
    Register tools that the LLM agent is allowed to request.
    """

    meeting_agent.register_for_llm(
        name="read_meeting_file",
        description=(
            "Read a local meeting transcript or notes file. "
            "Input: file_path. "
            "Output: a dictionary with success, file_path, content, and error. "
            "If success is false, report the error and end with TERMINATE. "
            "If success is true, use the content field as the meeting text."
        ),
    )(read_meeting_file)

    user_proxy.register_for_execution(
        name="read_meeting_file"
    )(read_meeting_file)


def create_agents() -> tuple[ConversableAgent, ConversableAgent]:
    """
    Create the agents used by the workflow.

    Returns:
        A tuple containing the meeting extraction agent and the user proxy.
    """

    meeting_agent = create_meeting_agent()
    user_proxy = create_user_proxy()

    register_tools(meeting_agent, user_proxy)

    return meeting_agent, user_proxy