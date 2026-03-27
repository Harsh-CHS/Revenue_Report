import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INCOMING_DIR = os.path.join(BASE_DIR, "incoming")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
ERROR_DIR = os.path.join(BASE_DIR, "error")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "automation.log")

for folder in [INCOMING_DIR, OUTPUT_DIR, PROCESSED_DIR, ERROR_DIR, LOG_DIR]:
    os.makedirs(folder, exist_ok=True)