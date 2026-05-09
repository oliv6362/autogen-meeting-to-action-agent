from autogen import ConversableAgent
from src.meeting_action_agent.config import LLM_CONFIG

def create_meeting_agent() -> ConversableAgent:
    meeting_agent = ConversableAgent(
        name="meeting_action_agent",
        system_message=(
            "You are an AI meeting-to-action assistant. "
            "Your task is to analyze meeting transcripts, notes, or messy project discussions "
            "and turn them into structured follow-up work. "
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
