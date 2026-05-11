from pathlib import Path

from src.meeting_action_agent.workflow import run_meeting_workflow


TEST_CASE_DIR = Path("evaluation/test_cases")
OUTPUT_DIR = Path("evaluation/outputs")


def main() -> None:
    """
    Run the Meeting-to-Action Agent on all fixed evaluation test cases.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    test_case_files = sorted(TEST_CASE_DIR.glob("*.txt"))

    if not test_case_files:
        print("No test cases found.")
        return

    for test_case_file in test_case_files:
        output_file = OUTPUT_DIR / f"{test_case_file.stem}_output.md"

        print(f"Running {test_case_file} -> {output_file}")

        result = run_meeting_workflow(
            input_file=str(test_case_file),
            output_file=str(output_file),
        )

        print(f"Finished {test_case_file.name}")
        print("-" * 80)

    print(f"Evaluation complete. Outputs saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()