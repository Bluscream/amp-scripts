import json
from logging import getLogger
from pathlib import Path
from typing import Dict, Any
from jsonpath_ng import jsonpath, parse, exceptions

class UniqueJsonParser:
    logger = getLogger(__name__)
    data: Dict[str, Any]

    def __init__(self):
        self.merged_dict: Dict[str, Any] = {}

    def add_file(self: 'UniqueJsonParser', json_file: Path, skip_errors: bool = False) -> list[str]: return self.add_files([json_file], skip_errors)
    def add_files(self: 'UniqueJsonParser', json_files: list[Path], skip_errors: bool = False) -> list[str]:
        errors = []
        for file in json_files:
            relative_path = file.relative_to(Path.cwd())
            self.logger.info(f"Processing file {relative_path}")
            _errors = self._merge_json_file(file = file, skip_errors = skip_errors, id=relative_path)
            self.logger.debug(f"Processed file {relative_path} with {len(_errors)} errors.")
            errors += _errors
        return errors

    def _merge_json_file(self: 'UniqueJsonParser', file: Path, skip_errors: bool = False, id: str = None) -> list[str]:
        errors = []
        if not isinstance(file, Path): file = Path(file)
        if not file.suffix.lower() == '.json':
            msg = f"[{id}] File {file} is probably not a JSON file."
            errors.append(msg)
            if skip_errors:
                self.logger.error(msg)
                return errors
            else: raise ValueError(msg)

        with open(file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                msg = f"[{id}] Failed to parse JSON file: {e}"
                errors.append(msg)
                if skip_errors:
                    self.logger.error(msg)
                    return errors
                else: raise ValueError(msg)
            if not isinstance(data, dict):
                msg = f"[{id}] Invalid JSON file: expected object, got {type(data)}"
                errors.append(msg)
                if skip_errors:
                    self.logger.error(msg)
                    return errors
                else: raise ValueError(msg)
            errors += self._merge_dict(data = data, skip_errors = skip_errors, id = id)
        return errors

    def _merge_dict(self, data: Dict[str, Any], skip_errors: bool = False, id: str = None, key_jpath: str = "$") -> list[str]:
        errors = []
        new_dict = self.merged_dict.copy()

        for key, value in data.items():
            # Construct the full path for the current key
            full_key_jpath = f"{key_jpath}.['{key}']"
            # self.logger.debug(f"[{id}] Processing key \"{full_key_jpath}\"")
            
            # Use jsonpath-ng to find if the full JSONPath already exists in the merged dictionary
            try: jsonpath_expr = parse(full_key_jpath)
            except exceptions.JsonPathParserError as ex:
                if " (NUMBER)" in str(ex): self.logger.error(ex)
                else: raise ex
            exists = jsonpath_expr.find(new_dict)
            if exists:
                msg = f"[{id}] Key \"{full_key_jpath}\" already exists in the merged dictionary."
                errors.append(msg)
                if skip_errors:
                    self.logger.error(msg)
                    continue
                else:
                    raise ValueError(msg)
            
            if isinstance(value, dict):
                # Ensure the key in the merged dictionary is also a dict before merging
                if exists and not isinstance(new_dict[key], dict):
                    msg = f"[{id}] Key \"{full_key_jpath}\" is not a dictionary in the merged dictionary."
                    errors.append(msg)
                    if skip_errors:
                        self.logger.error(msg)
                        continue
                    else:
                        raise ValueError(msg)
                
                # Recursive call for nested dictionaries, passing the full path for the current key
                errors += self._merge_dict(value, skip_errors=skip_errors, id=id, key_jpath=full_key_jpath)
            else:
                new_dict[key] = value
        
        if not new_dict:
            msg = f"[{id}] Failed to merge dictionary. (new_dict is empty)."
            errors.append(msg)
            if not skip_errors:
                raise ValueError(msg)
        else:
            self.merged_dict = new_dict
        
        return errors