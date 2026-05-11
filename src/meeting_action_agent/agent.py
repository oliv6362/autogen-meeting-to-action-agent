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
            "You are a meeting-to-action extraction agent. "
            "When given a meeting file path, you must call the read_meeting_file tool. "
            "After read_meeting_file returns success=true, your next response must start with a JSON object. "
            "Do not wait for another user message. "
            "Do not send an empty response. "
            "Do not return Markdown, explanations, or extra text. "
            "Return only the JSON object requested by the workflow, followed by TERMINATE on a separate line. "
            "Do not invent information. "
            "Use evidence quotes from the meeting text for every extracted decision, action item, open question, and risk."
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