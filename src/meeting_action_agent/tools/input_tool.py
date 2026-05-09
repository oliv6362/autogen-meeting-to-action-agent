from pathlib import Path


def read_meeting_file(file_path: str) -> str:
    """
    Read a local meeting transcript or notes file.

    Args:
        file_path: Path to a .txt or .md meeting file.

    Returns:
        The raw meeting text from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is unsupported or the file is empty.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Meeting file not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    if path.suffix.lower() not in {".txt", ".md"}:
        raise ValueError(
            f"Unsupported file type: {path.suffix}. Only .txt and .md files are supported."
        )

    meeting_text = path.read_text(encoding="utf-8").strip()

    if not meeting_text:
        raise ValueError(f"Meeting file is empty: {file_path}")

    return meeting_text