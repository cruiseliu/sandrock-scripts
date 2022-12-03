from sandrock import *
from sandrock.lib.asset import Bundle

def find_configs():
    configs = {
        'text': {},
        'designer_config': None,
    }
    for lang in config.languages:
        configs['text'][lang] = _find_text(config.assets_root / 'localization' / lang)
    configs['designer_config'] = _find_designer_configs(config.assets_root / 'designer_config')
    return configs

def _find_designer_configs(designer_config_path):
    bundle = Bundle(designer_config_path)
    key_to_path = {}
    for behav in bundle.behaviours:
        key = behav.data['key']
        key_to_path[key] = str(behav.path)
    return sorted_dict(key_to_path)

def _find_text(language_path):
    bundle = Bundle(language_path)
    for behav in bundle.behaviours:
        if behav.script == 'AssetItem':
            return str(behav.path)
