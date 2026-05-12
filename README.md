# AutoGen Meeting-to-Action Agent

AutoGen exam project for the 2026 **Machine Learning** course.

The agent reads a meeting transcript from a local file, extracts structured follow-up information, validates the result with deterministic Python checks, formats the output as a Markdown report, and logs tool calls.

The system extracts:

- Decisions
- Action items
- Owners
- Deadlines
- Open questions
- Risks
- Supporting evidence quotes

## Project Goal

The goal of this project is to build a bounded AI agentic system that uses external data and tools to turn meeting transcripts, notes, or messy discussions into structured follow-up work.

The final output is grounded in the retrieved meeting text through evidence quotes from the transcript.

## Tools

The project uses three tools:

| Tool | Purpose |
|---|---|
| read_meeting_file | Reads a local .txt or .md meeting transcript file. |
| validate_meeting_output | Validates the extracted structured data using Pydantic and deterministic checks. |
| format_meeting_report | Formats validated meeting data into a readable Markdown report. |

The LLM agent calls read_meeting_file through AutoGen.

Validation and formatting are handled deterministically by the workflow.

## Workflow

The workflow is orchestrated in src/meeting_action_agent/workflow.py.

The process is:

1. The workflow creates the AutoGen agents.
2. The LLM agent receives a file path.
3. The LLM agent calls read_meeting_file.
4. The LLM extracts structured JSON from the returned meeting text.
5. The workflow parses the JSON response.
6. The workflow validates the extracted data with validate_meeting_output.
7. If validation succeeds, the workflow formats the final report with format_meeting_report.
8. The final Markdown report is saved to the output path.
9. Tool calls are logged to logs/tool_calls.jsonl.

## Project Structure

```text
AutoGenMeetingToActionAgent/
├── main.py
├── evaluate.py
├── data/
│   └── sample_meetings/
│       └── demo_meeting.txt
├── generated/
│   └── meeting_report.md
├── evaluation/
│   ├── evaluation_results.md
│   ├── test_cases/
│   └── outputs/
├── logs/
│   └── tool_calls.jsonl
└── src/
    └── meeting_action_agent/
        ├── agent.py
        ├── config.py
        ├── logger.py
        ├── models.py
        ├── workflow.py
        └── tools/
            ├── formatter_tool.py
            ├── input_tool.py
            └── validation_tool.py
```

## Prerequisites

- The project was developed using Python 3.12 in a Miniconda3 environment.
- Make sure Ollama is installed and running locally.
- Make sure you have pulled the configured Ollama model. 
   
For example:
    
    Ollama pull gemma4:latest


## Requirements & Installation

- You do not need to install any requirement.txt file, instead you just need to import the envirment.yml file.

Import the Conda environment from the environment.yml file from the project root folder:

    conda env create --file environment.yml

Activate the Conda environment:

    conda activate AutoGenMeetingToActionAgent

If necessary, remove the Conda environment with:

    conda env remove -n AutoGenMeetingToActionAgent

## Configuration

The local LLM configuration is defined in:

    src/meeting_action_agent/config.py

Example Ollama configuration:

    LLM_CONFIG = {
        "config_list": [
            {
                "model": "gemma4:latest",
                "api_type": "ollama",
                "client_host": "http://127.0.0.1:11434",
                "native_tool_calls": False,
            }
        ],
        "temperature": 0.1,
        "seed": 42,
        "cache_seed": None,
    }

The default input and output paths are also configured in this file:

    LOG_DIR = "logs"
    DEFAULT_INPUT_FILE = "data/sample_meetings/demo_meeting.txt"
    DEFAULT_OUTPUT_FILE = "generated/meeting_report.md"

## Run the Agent

From the project root, run:

    python main.py

By default, this reads:

    data/sample_meetings/demo_meeting.txt

And writes the generated report to:

    generated/meeting_report.md

You can also provide a custom input and output file:

    python main.py --input data/sample_meetings/demo_meeting.txt --output generated/meeting_report.md

## Run the Evaluation

From the project root, run:

    python evaluate.py

This runs the agent on all fixed test cases in:

    evaluation/test_cases/

And writes the generated outputs to:

    evaluation/outputs/

A short evaluation summary is available at:

    evaluation/evaluation_results.md

Tool calls are logged to:

    logs/tool_calls.jsonl

## Evaluation

The agent was evaluated on 10 fixed meeting transcript test cases.

See the evaluation summary here:

[Evaluation Results](evaluation/evaluation_results.md)