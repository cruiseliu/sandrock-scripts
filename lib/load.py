from .common import *
from .asset import Bundle
from .preproc import get_config_paths

from functools import cache
from xml.etree import ElementTree

@cache
def load_text(language):
    config_paths = get_config_paths()
    path = config_paths['text'][language]
    data = read_json(path)
    configs = data['configList']
    texts = {config['id']: config['text'] for config in configs}
    return dict(sorted(texts.items()))


@cache
def load_config(key):
    config_paths = get_config_paths()
    path = config_paths['designer_config'][key]
    data = read_json(path)
    configs = data['configList']
    if not configs:
        return None
    if isinstance(configs[0].get('id'), int):
        config_dict = {conf['id']: conf for conf in configs}
        return dict(sorted(config_dict.items()))
    elif isinstance(configs[0].get('ID'), int):
        config_dict = {conf['ID']: conf for conf in configs}
        return dict(sorted(config_dict.items()))
    else:
        return configs

class _ConfigLoader:
    def __getattr__(self, key):
        return _ConfigWrapper(load_config(key))

    def __getitem__(self, key):
        return _ConfigWrapper(load_config(key))

class _ConfigWrapper:
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        if isinstance(self._data, dict):
            return iter(self._data.values())
        else:
            return iter(self._data)

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def get(self, key):
        return self._data.get(key)

DesignerConfig = _ConfigLoader()
