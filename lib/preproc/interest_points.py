from sandrock import *
from sandrock.lib.asset import Bundle

_interest_scripts = [
    'DestroyableSceneItemPoint',
    'ResourceArea',
    'SceneItemBox',
    'SpawnMono_Point',
]

def find_interest_points():
    interests = []
    scenes_dir = config.assets_root / 'scene/additive'
    scenes = sorted(scenes_dir.iterdir())
    #additional_areas = _get_additional_resource_areas()
    for scene in scenes:
        interests += _find_scene_interests(scene)
    return interests

def _find_scene_interests(scene_path):
    bundle = Bundle(scene_path)
    interests = []
    for behav in bundle.behaviours:
        if behav.script in _interest_scripts:
            interest = {
                'scene': scene_path.name,
                'id': behav.game_object.id,
                'type': behav.script,
                'behaviour': str(behav.path),
                'transform': str(behav.game_object.transform.path),
            }
            for comp in behav.game_object.components:
                if comp.type == 'MonoBehaviour' and comp.script == 'SceneArea':
                    interest['scene_area'] = str(comp.path)
            interests.append(interest)
    return interests

def _get_additional_resource_areas():
    bundle = Bundle(config.assets_root / 'resourceareainfo')
    areas = {}
    for asset in bundle.assets:
        if asset.type == 'MonoBehaviour' and asset.script == 'ResourceAreaInfoObj':
            for area in asset.data['resourceAreaConfigs']:
                name = area['sceneAreaName']
                assert name not in areas
                areas[name] = asset.path
    return areas
