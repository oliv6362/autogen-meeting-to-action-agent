import argparse

from src.meeting_action_agent.config import DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_FILE
from src.meeting_action_agent.workflow import run_meeting_workflow


def main() -> None:
    """
    Command-line entry point for the AutoGen Meeting-to-Action Agent.
    """

    parser = argparse.ArgumentParser(
        description="Run the AutoGen Meeting-to-Action Agent on a meeting transcript."
    )

    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_FILE,
        help="Path to the meeting transcript or notes file.",
    )

    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help="Path where the generated Markdown report should be saved.",
    )

    args = parser.parse_args()

    result = run_meeting_workflow(
        input_file=args.input,
        output_file=args.output,
    )

    print(result)


if __name__ == "__main__":
    main()