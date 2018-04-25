
import logging
import sys
import os

if sys.version > "3":
    PY2 = False
else:
    PY2 = True


__version__ = '0.3.0'
__all__ = ['hive_client', 'Jump_Tunnel_HIVE', 'SSH_Tunnel']


# Initialize logger.
logger = logging.getLogger("ssh-jump-hive")
logger.setLevel(logging.INFO)
console_hdlr = logging.StreamHandler()
console_hdlr.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)s   %(levelname)-8s %(message)s")
console_hdlr.setFormatter(formatter)
logger.addHandler(console_hdlr)
