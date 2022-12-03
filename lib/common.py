from sandrock import config
#from .dump import lua_dump, yaml_dump

from collections import defaultdict
from dataclasses import dataclass
from functools import cache
import json
from pathlib import Path
from xml.etree import ElementTree

def sorted_dict(dict_, key=None):
    return dict(sorted(dict_.items(), key=key))

def read_json(path):
    with open(path) as f:
        return json.load(f)

def write_raw(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        path.write_text(data)
    else:
        path.write_bytes(data)

def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def write_yaml(path, data, indent=4):
    if isinstance(indent, int):
        indent = ' ' * indent
    s = yaml_dump(data, '', indent)
    if isinstance(s, list):
        s = '\n'.join(s)

    path = Path(path)
    if not path.is_absolute():
        path = config.output_dir / path

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(s)

def write_lua(path, data, indent='\t'):
    if isinstance(indent, int):
        indent = ' ' * indent
    s = 'return ' + lua_dump(data, '', indent)

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(s)

def write_xml(path, root):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    ElementTree.ElementTree(root).write(path, 'utf_8')
