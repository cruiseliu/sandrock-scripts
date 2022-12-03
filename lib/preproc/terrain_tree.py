from sandrock import *
from sandrock.lib.asset import Bundle

def find_terrain_trees():
    trees = []
    scene_dir = (config.assets_root / 'scene/additive')
    for scene in sorted(scene_dir.iterdir()):
        trees += find_scene_trees(scene)
    season_dir = (config.assets_root / 'season')
    for season in sorted(season_dir.iterdir()):
        trees += find_scene_trees(season)
    return trees

def find_scene_trees(scene_path):
    bundle = Bundle(scene_path)

    game_objs = {}
    for asset in bundle.assets:
        if asset.type == 'GameObject' and asset.name:
            game_objs[asset.id] = asset

    trees = []

    for asset in bundle.assets:
        if asset.type != 'TerrainData':
            continue

        db = asset.data['m_DetailDatabase']
        prototypes = db['m_TreePrototypes']
        instances = db['m_TreeInstances']

        for instance in instances:
            proto = prototypes[instance['index']]
            prefab_id = proto['prefab']['m_PathID']
            obj = game_objs[prefab_id]
            trees.append({
                'scene': scene_path.name,
                'prefab': obj.name,
                'position': instance['position'],
            })

    return trees
