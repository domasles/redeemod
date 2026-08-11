from pathlib import Path


def append_to_ini_file(path: Path, section: str, new_content: str) -> None:
    """Append new paths to an .ini file under the specified section."""

    with open(path, "r") as f:
        content = f.read()

    head, tail = content.split(f"[{section}]\n", 1)

    if "\n[" in tail:
        section_body, rest = tail.split("\n[", 1)
        content = f"{head}[{section}]\n{section_body.strip()}\n{new_content}\n\n[{rest}"

    else:
        content = f"{head}[{section}]\n{tail.strip()}\n{new_content}\n"

    with open(path, "w") as f:
        f.write(content)
