import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

CONFIG_URL = os.path.join(ROOT_DIR, "app", "config", "config.json")
with open(CONFIG_URL, "r", encoding="utf-8") as f:
    config = json.load(f)

DB_URL = os.path.join(ROOT_DIR, *config["DB_URL"].split("/"))
DB_URL = f"sqlite:///{DB_URL}"
