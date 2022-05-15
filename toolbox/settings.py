import os

# Loads environment variables from .env file:
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            os.environ.setdefault(key, value)

ACCOUNT = str(os.environ["ALWAYSDATA_ACCOUNT"])
APIKEY = str(os.environ["ALWAYSDATA_APIKEY"])
DDNS_TOKEN = str(os.environ["DDNS_TOKEN"])
