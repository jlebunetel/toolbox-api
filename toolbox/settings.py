import os
from io import TextIOWrapper
from pathlib import Path
from typing import Generator


def reader(text_stream: TextIOWrapper) -> Generator[tuple[str, str], None, None]:
    for row in filter(lambda row: row.strip() and not row.startswith("#"), text_stream):
        # void rows and rows starting with '#' are skiped

        # remove the endline character '\n'
        cleaned_row: str = row.rstrip()

        # get key value tuple
        k, v = cleaned_row.split("=", 1)

        # remove leading and trailing '"' characters
        v = v.strip('"')

        # yield cleaned values
        yield k, v


# Loads environment variables from .env file (if not already set):
if os.path.exists(".env"):
    with open(".env", mode="r", encoding="utf_8", errors="strict") as stream:
        for key, value in reader(stream):
            if key not in os.environ:
                os.environ.setdefault(key, value)

# Get environment variables
ACCOUNT = str(os.environ["ALWAYSDATA_ACCOUNT"])
APIKEY = str(os.environ["ALWAYSDATA_APIKEY"])
DDNS_TOKEN = str(os.environ["DDNS_TOKEN"])

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
FAVICON = BASE_DIR / "favicon.ico"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
