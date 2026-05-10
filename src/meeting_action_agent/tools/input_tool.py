from pathlib import Path
from typing import Any

from src.meeting_action_agent.logger import log_tool


SUPPORTED_FILE_TYPES = {".txt", ".md"}

@log_tool("read_meeting_file")
def read_meeting_file(file_path: str) -> dict[str, Any]:
    """
    Read a local meeting transcript or notes file.

    Args:
        file_path: Path to a .txt or .md meeting file.

    Returns:
        A dictionary containing:
        - success: Whether the file was read successfully.
        - file_path: The provided file path.
        - content: The meeting text if successful.
        - error: Error message if unsuccessful.
    """

    path = Path(file_path)

    if not path.exists():
        return {
            "success": False,
            "file_path": file_path,
            "content": "",
            "error": f"Meeting file not found: {file_path}",
        }

    if not path.is_file():
        return {
            "success": False,
            "file_path": file_path,
            "content": "",
            "error": f"Path is not a file: {file_path}",
        }

    if path.suffix.lower() not in SUPPORTED_FILE_TYPES:
        return {
            "success": False,
            "file_path": file_path,
            "content": "",
            "error": (
                f"Unsupported file type: {path.suffix}. "
                "Only .txt and .md files are supported."
            ),
        }

    meeting_text = path.read_text(encoding="utf-8").strip()

    if not meeting_text:
        return {
            "success": False,
            "file_path": file_path,
            "content": "",
            "error": f"Meeting file is empty: {file_path}",
        }

    return {
        "success": True,
        "file_path": file_path,
        "content": meeting_text,
        "error": "",
    }