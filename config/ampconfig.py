from logging import getLogger
from pathlib import Path
from shutil import copy2
from .ampconfigline import AMPConfigLine

class AMPConfig:
    path: Path
    raw: list[str]
    lines: list[AMPConfigLine]
    logger = getLogger(__name__)

    def __init__(self, path: Path) -> None:
        self.path = path
        self.load(path)

    def load(self, path: Path = None) -> None:
        path = path or self.path
        with open(path, 'r') as f:
            self.raw = f.readlines()
        self.lines = [AMPConfigLine(line) for line in self.raw]
        self.logger.debug(f'Loaded {len(self.lines)} lines from {path}')

    def save(self, path: Path = None, backup: bool = True) -> None:
        path = path or self.path
        if backup: self.backup()
        with open(path, 'w') as f:
            lines = [str(line) for line in self.lines]
            for line in lines:
                f.write(line+'\n')
            self.logger.debug(f'Saved {len(self.lines)} lines to {path}')

    def backup(self, force: bool = False) -> None:
        backup_path = self.path.with_suffix('.bak')
        if not backup_path.is_file() or force:
            self.logger.debug(f'Backing up {self.path} to {backup_path}')
            copy2(self.path, backup_path)

    def update_config(self, replacements: list[AMPConfigLine]) -> None:
        self.logger.debug(f'Updating {self.path} with {replacements}')
        for replacement in replacements:
            for i, line in enumerate(self.lines):
                if line.key == replacement.key:
                    self.lines[i] = replacement
                    break