import re

from pathlib import Path


def prepend_to_ini_section(path: str | Path, section: str, new_content: str) -> str:
    """Inserts new lines directly under the specified INI section header."""

    path_obj = Path(path)
    content = path_obj.read_text(encoding="utf-8")

    pattern = re.compile(rf"^\[{re.escape(section)}\]\r?$", re.MULTILINE | re.IGNORECASE)
    match = pattern.search(content)

    if not match:
        raise ValueError(f"Section [{section}] not found in {path_obj}")

    insert_idx = match.end()

    head = content[:insert_idx].rstrip("\r\n")
    tail = content[insert_idx:].lstrip("\r\n")

    return f"{head}\n{new_content.strip()}\n{tail}"
