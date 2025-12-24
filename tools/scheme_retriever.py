import json
import os

SCHEME_FILE = os.path.join(os.path.dirname(__file__), "schemes.json")


def load_schemes():
    if not os.path.exists(SCHEME_FILE):
        raise FileNotFoundError("schemes.json not found")

    with open(SCHEME_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# 🧪 TEST
if __name__ == "__main__":
    schemes = load_schemes()
    for s in schemes:
        print(s["name"])
