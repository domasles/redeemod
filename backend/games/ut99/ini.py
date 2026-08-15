import re

from pathlib import Path


def append_to_ini_file(path: str | Path, section: str, new_content: str) -> str:
    """Append new lines under the specified INI section."""

    path_obj = Path(path)
    content = path_obj.read_text(encoding="utf-8")

    pattern = re.compile(rf"^\[{re.escape(section)}\]\r?$", re.MULTILINE | re.IGNORECASE)
    match = pattern.search(content)

    if not match:
        raise ValueError(f"Section [{section}] not found in {path_obj}")

    start_idx = match.end()

    # Find next section start or match end of file
    next_section = re.search(r"^\[.*\]\r?$", content[start_idx:], re.MULTILINE)
    split_point = (start_idx + next_section.start()) if next_section else len(content)

    head = content[:split_point].rstrip()
    tail = content[split_point:]

    separator = "\n\n" if tail else "\n"

    return f"{head}\n{new_content.strip()}{separator}{tail}"
