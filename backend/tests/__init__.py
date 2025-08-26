import os
import sys
import pathlib

# Allow `pytest` discovery when running from /backend
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
