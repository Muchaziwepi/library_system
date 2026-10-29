"""File handling: saves and loads the whole library as one JSON file."""

import json
import os

from exceptions import LibraryError


class StorageError(LibraryError):
    """Raised when the data file cannot be read or written."""


EMPTY_DATA = {"books": [], "members": [], "records": []}


def load_data(path: str) -> dict:
    """Return stored data, or an empty structure if the file doesn't exist yet."""
    if not os.path.exists(path):
        return {key: [] for key in EMPTY_DATA}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise StorageError(
            f"'{path}' is corrupted. Fix or delete it, then restart.") from None
    except OSError as e:
        raise StorageError(f"Could not read '{path}': {e}") from None

    for key in EMPTY_DATA:          # make sure every section exists
        data.setdefault(key, [])
    return data


def save_data(path: str, data: dict) -> None:
    """Write to a temp file first, then replace, so a crash can't wipe the data."""
    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, path)
    except OSError as e:
        raise StorageError(f"Could not save data: {e}") from None
