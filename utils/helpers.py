"""File I/O helpers with error handling."""
import json
import logging
import os

logger = logging.getLogger(__name__)


def load_data(filepath):
    """Load a JSON list from filepath.

    Returns [] if the file is missing or empty. If the file contains
    malformed JSON, a warning is logged and [] is returned instead of crashing.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []
            data = json.loads(content)
    except json.JSONDecodeError as error:
        logger.warning("Malformed JSON in %s: %s", filepath, error)
        return []
    except OSError as error:
        logger.warning("Could not read %s: %s", filepath, error)
        return []
    if not isinstance(data, list):
        logger.warning("Expected a list in %s", filepath)
        return []
    return data


def save_data(filepath, data):
    """Write data as pretty JSON, creating the folder if needed."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
