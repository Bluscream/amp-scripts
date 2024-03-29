import shutil
import urllib.request
import subprocess
import json
import logging
from copy import copy
from datetime import datetime
from pathlib import Path

from config import AMPConfig, AMPConfigLine

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
    orig_cfg = AMPConfig(Path('amp/test/AMPConfig.conf'))
    orig_cfg.save('amp/test/AMPConfig_patched.conf')
    pass