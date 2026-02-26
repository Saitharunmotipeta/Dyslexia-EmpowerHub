from pathlib import Path

BASE_PATH = Path("temp/reports")
BASE_PATH.mkdir(parents=True, exist_ok=True)


def save_report_file(filename: str, content: bytes) -> Path:
    path = BASE_PATH / filename
    with open(path, "wb") as f:
        f.write(content)
    return path