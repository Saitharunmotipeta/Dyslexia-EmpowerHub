import os


def cleanup_file(path: str):
    if path and os.path.exists(path):
        os.remove(path)
