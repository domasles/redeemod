import zlib

from zipfile import ZipFile
from pathlib import Path


def calculate_archive_adler32(path: Path) -> int:
    """Calculates Adler-32 checksum of files within an archive."""

    adler = 1

    try:
        with ZipFile(path, "r") as zf:
            for info in zf.infolist():
                if info.file_size > 0:
                    adler = zlib.adler32(f"{info.filename}:{info.CRC}\n".encode(), adler)

    except Exception:
        return 0

    return adler
