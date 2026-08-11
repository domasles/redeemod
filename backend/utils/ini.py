from pathlib import Path


def append_to_ini_file(path: Path, section: str, new_content: str) -> str:
    """Append new paths to an .ini file under the specified section and return the updated content."""

    with open(path, "r") as f:
        content = f.read()

    head, tail = content.split(f"[{section}]\n", 1)

    section_body, sep, rest = tail.partition("\n[")
    content = f"{head}[{section}]\n{section_body.strip()}\n{new_content}\n{sep}{rest}"

    return content
