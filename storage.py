import json
from pathlib import Path

from library_service import LibraryManager


def load_data(file_name):
    path = Path(file_name)
    if not path.exists():
        return LibraryManager()

    try:
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            return LibraryManager()
        return LibraryManager.from_dict(json.loads(text))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"Could not load data: {error}")
        return LibraryManager()


def save_data(library, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(library.to_dict(), file, indent=4)
