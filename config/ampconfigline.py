from json import loads, JSONDecodeError
from typing import Any, Optional


def parse_value(value: str) -> Any:
    if value.lower() in ['true','yes','on','enabled']: return True
    elif value.lower() in ['false','no','off','disabled']: return False
    elif value.isdigit(): return int(value)
    try: return float(value)
    except ValueError: pass
    try: return loads(value)
    except JSONDecodeError: pass
    return str(value)

class AMPConfigLine:
    raw: str = ''
    comment: Optional[str] = None
    key: Optional[str] = None
    value: Optional[Any] = None

    def __init__(self, line: str) -> None:
        line = line.strip()
        self.raw = line
        items = line.split('#', 1)
        if len(items) > 1: self.comment = items[-1].strip()
        items = items[0].split('=', 1)
        if len(items) > 0:
            self.key = items[0].strip()
            if len(items) > 1: self.value = parse_value(items[1].strip())
        
    def __str__(self) -> str:
        ret = ''
        if self.key: ret += f'{self.key}'
        if self.value: ret += f'={self.value}'
        if self.key or self.value and self.comment: ret += ' '
        if self.comment:
            ret += f'# {self.comment}'
        return ret