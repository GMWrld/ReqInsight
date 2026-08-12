import os

from dotenv import load_dotenv


load_dotenv()


ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)

MAX_FILE_SIZE_MB = int(
    os.getenv(
        "MAX_FILE_SIZE_MB",
        "10"
    )
)

MAX_FILE_SIZE = (
    MAX_FILE_SIZE_MB * 1024 * 1024
)


ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000"
    ).split(",")
    if origin.strip()
]