from typing import Optional
from enum import Enum
from typing import Any
from dataclasses import dataclass
from json import loads as json_loads, dumps as json_dumps
from logging import getLogger
from pathlib import Path
from shutil import copy2
from utils import get_safe


class TemplateConfigItem:
    display_name: str
    category: str = "Server Settings"
    description: str
    keywords: str
    field_name: str
    input_type: str
    is_flag_argument: Optional[bool]
    param_field_name: str
    include_in_command_line: Optional[bool]
    default_value: str
    placeholder: Optional[str]
    suffix: Optional[str]
    hidden: Optional[bool]
    skip_if_empty: Optional[bool]
    enum_values: Optional[dict[str,Any]]

    # def __init__(self):
    #     self.display_name

    def __init__(self, display_name: str, category: str, description: str, keywords: str, field_name: str, input_type: str, is_flag_argument: bool, param_field_name: str, include_in_command_line: bool, default_value: str, placeholder: str, suffix: str, hidden: bool, skip_if_empty: bool, enum_values: dict[str,Any]) -> None:
        self.display_name = display_name
        self.category = category
        self.description = description
        self.keywords = keywords
        self.field_name = field_name
        self.input_type = input_type
        self.is_flag_argument = is_flag_argument
        self.param_field_name = param_field_name
        self.include_in_command_line = include_in_command_line
        self.default_value = default_value
        self.placeholder = placeholder
        self.suffix = suffix
        self.hidden = hidden
        self.skip_if_empty = skip_if_empty
        self.enum_values = enum_values

    @staticmethod
    def from_dict(obj: dict[str, Any]) -> 'TemplateConfigItem':
        if not obj: return None
        _DisplayName = get_safe(obj, "DisplayName")
        _Category = get_safe(obj, "Category")
        _Description = get_safe(obj, "Description")
        _Keywords = get_safe(obj, "Keywords")
        _FieldName = get_safe(obj, "FieldName")
        _InputType = get_safe(obj, "InputType")
        _IsFlagArgument = get_safe(obj, "IsFlagArgument")
        _ParamFieldName = get_safe(obj, "ParamFieldName")
        _IncludeInCommandLine = get_safe(obj, "IncludeInCommandLine")
        _DefaultValue = get_safe(obj, "DefaultValue")
        _Placeholder = get_safe(obj, "Placeholder")
        _Suffix = get_safe(obj, "Suffix")
        _Hidden = get_safe(obj, "Hidden")
        _SkipIfEmpty = get_safe(obj, "SkipIfEmpty")
        _EnumValues = get_safe(obj, "EnumValues")
        return TemplateConfigItem(_DisplayName, _Category, _Description, _Keywords, _FieldName, _InputType, _IsFlagArgument, _ParamFieldName, _IncludeInCommandLine, _DefaultValue, _Placeholder, _Suffix, _Hidden, _SkipIfEmpty, _EnumValues)



class TemplateConfig:
    path: Path
    raw: dict[str, Any]
    items: list['TemplateConfigItem']
    logger = getLogger(__name__)

    def __init__(self, path: Path) -> None:
        self.path = path
        self.load(path)

    def load(self, path: Path = None) -> None:
        path = path or self.path
        with open(path, 'r') as f:
            self.raw = json_loads(f.read())
        self.items = [TemplateConfigItem.from_dict(item) for item in self.raw]
        self.logger.debug(f'Loaded {len(self.items)} items from {path}')

    def save(self, path: Path = None, backup: bool = True) -> None:
        path = path or self.path
        if backup: self.backup()
        with open(path, 'w') as f:
            f.write(json_dumps(self.raw, indent=4))
            self.logger.debug(f'Saved {len(self.items)} items to {path}')

    def backup(self, force: bool = False) -> None:
        backup_path = self.path.with_suffix('.bak')
        if not backup_path.is_file() or force:
            self.logger.debug(f'Backing up {self.path} to {backup_path}')
            copy2(self.path, backup_path)