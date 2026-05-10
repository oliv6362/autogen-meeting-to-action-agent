import functools
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, TypeVar, cast

from src.meeting_action_agent.config import LOG_DIR


F = TypeVar("F", bound=Callable[..., Any])


def log_tool_call(tool_name: str, tool_input: dict[str, Any], tool_output: Any) -> None:
    """
    Log a tool call as one JSON line.
    """

    log_path = Path(LOG_DIR) / "tool_calls.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "tool_name": tool_name,
        "input": tool_input,
        "output": tool_output,
    }

    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


def log_tool(tool_name: str) -> Callable[[F], F]:
    """
    Decorator for logging deterministic tool calls.
    """

    def decorator(function: F) -> F:
        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            tool_input = {
                "args": args,
                "kwargs": kwargs,
            }

            tool_output = function(*args, **kwargs)

            log_tool_call(
                tool_name=tool_name,
                tool_input=tool_input,
                tool_output=tool_output,
            )

            return tool_output

        return cast(F, wrapper)

    return decorator