import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "prompt.txt")

with open(PROMPT_PATH, "r") as f:
    PROMPT_TEMPLATE = f.read()