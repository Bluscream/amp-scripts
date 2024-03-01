import json
from logging import getLogger
from pathlib import Path
from typing import Dict, Any

class UniqueJsonParser:
    logger = getLogger(__name__)
    data: Dict[str, Any]

    def __init__(self):
        self.merged_dict: Dict[str, Any] = {}

    def add_file(self: 'UniqueJsonParser', json_file: Path, skip_errors: bool = False) -> list[str]: return self.add_files([json_file], skip_errors)
    def add_files(self: 'UniqueJsonParser', json_files: list[Path], skip_errors: bool = False) -> list[str]:
        errors = []
        for file in json_files:
            errors += self._merge_json_file(file, skip_errors)
        return errors

    def _merge_json_file(self: 'UniqueJsonParser', file_path: Path, skip_errors: bool = False) -> list[str]:
        errors = []
        if not isinstance(file, Path): file = Path(file)
        if not file.suffix.lower() == '.json':
            msg = f"File {file} is probably not a JSON file."
            errors.append(msg)
            if skip_errors: return errors
            else: raise ValueError(msg)

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                msg = f"Failed to parse JSON file {file_path}: {e}"
                errors.append(msg)
                if skip_errors: return errors
                else: raise ValueError(msg)
            if not isinstance(data, dict):
                msg = f"Invalid JSON file {file_path}: expected object, got {type(data)}"
                errors.append(msg)
                if skip_errors: return errors
                else: raise ValueError(msg)

            errors += self._merge_dict(data)
        return errors

    def _merge_dict(self: 'UniqueJsonParser', data: Dict[str, Any], skip_errors: bool = False) -> list[str]:
        errors = []
        new_dict = self.merged_dict.copy()

        for key, value in data.items():
            if key in new_dict:
                msg = f"Key '{key}' already exists in the merged dictionary."
                errors.append(msg)
                if skip_errors: continue
                else: raise ValueError(msg)
            if isinstance(value, dict):
                if key in new_dict and not isinstance(new_dict[key], dict):
                    msg = f"Key '{key}' is not a dictionary in the merged dictionary."
                    errors.append(msg)
                    if skip_errors: continue
                    else: raise ValueError(msg)
                errors += self._merge_dict(value)
            else:
                new_dict[key] = value
        if not new_dict:
            msg = f"Failed to merge dictionary. (new_dict is empty)."
            errors.append(msg)
            if not skip_errors: raise ValueError(msg)
        else: self.merged_dict = new_dict
        return errors