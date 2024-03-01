import shutil
import urllib.request
import subprocess
import json
import logging
from copy import copy
from datetime import datetime
from pathlib import Path

from config import TemplateConfig, UniqueJsonParser

from typing import Any, Optional, Union
PathLike = Union[str, Path]

self: Path = Path(__file__).resolve()

log_format = '%(asctime)s - %(levelname)s - %(message)s'
file_handler = logging.FileHandler(self.parent / f'{self.name}.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(log_format))
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler])
logger = logging.getLogger(__name__)
logger.debug(f'Logging started at {datetime.now()}')
logger.debug(f'Script location: {self}')

if __name__ == '__main__':

    base_dir = self.parent / 'test'

    templateCfg = TemplateConfig(base_dir / 'iw4madminconfig.json')
    logger.debug(f'Loaded {len(templateCfg.items)} items from {templateCfg.path}')
    json_dir = base_dir / 'Configuration'
    json_files = list(json_dir.glob('**/*.json'))
    logger.debug(f'Found {len(json_files)} JSON files in {json_dir}')

    merger = UniqueJsonParser()
    errors = merger.add_files(json_files, skip_errors=True)
    logger.debug(f'Found {len(errors)} errors in {len(json_files)} files')
    # for error in errors:
        # logger.error(error)
    print(merger.merged_dict)

    # orig_cfg.save('amp/test/AMPConfig_patched.conf')
    pass