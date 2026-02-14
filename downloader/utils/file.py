"""module downloader.utils.file"""

import json
from typing import Union, List, Dict
from downloader.logger_config import get_logger

logger = get_logger(__name__)


def save_data_to_json_file(data: Union[str, List, Dict], json_file_path: str) -> bool:
    """Save data to a JSON file.

    Args:
        data (Union[str, List, Dict]): The data to be saved.
        json_file_path (str): The path to the file where the data will be saved.

    Returns:
        bool: True if the data was saved successfully, False otherwise.
    """
    try:
        with open(json_file_path, "w", encoding="utf-8") as file:
            if isinstance(data, (dict, list)):
                json.dump(data, file, indent=4, ensure_ascii=False)
            else:
                file.write(data)
        logger.info("Data successfully saved to %s", json_file_path)
        return True
    except PermissionError:
        logger.error("Permission denied: Cannot write to %s", json_file_path)
    except FileNotFoundError:
        logger.error("Directory not found for file: %s", json_file_path)
    except IsADirectoryError:
        logger.error("Path is a directory, not a file: %s", json_file_path)
    except OSError as e:
        logger.error("OS error occurred while saving to %s: %s", json_file_path, e)
    except TypeError as e:
        logger.error("Type error: Data must be a string, dict or list. %s", e)
    except Exception as e:
        logger.error("Unexpected error saving to %s: %s", json_file_path, e)
    return False
