from sandrock import config
from ..common import *

@cache
def get_config_paths():
    from .configs import find_configs
    return _presistent_cached('config_path', find_configs)

@cache
def get_interest_points():
    from .interest_points import find_interest_points
    return _presistent_cached('interest_points', find_interest_points)

@cache
def get_catchable_resource_points():
    from .catchable_resource import find_catchable_resource_points
    return _presistent_cached('salvaging_resource_points', find_catchable_resource_points)

@cache
def get_terrain_trees():
    from .terrain_tree import find_terrain_trees
    return _presistent_cached('terrain_trees', find_terrain_trees)

@cache
def get_mission_names():
    from .mission import find_mission_names
    data = _presistent_cached('mission_name', find_mission_names)
    return {int(k): v for k, v in data.items()}

def _presistent_cached(cache_key, func, update=False):
    cache_path = config.cache_root / f'{cache_key}.json'
    if not update and cache_path.exists():
        try:
            cache = read_json(cache_path)
            if cache['version'] == config.version:
                return cache['data']
        except Exception:
            pass
    data = func()
    cache = {
        'version': config.version,
        'data': data,
    }
    write_json(cache_path, cache)
    return data
