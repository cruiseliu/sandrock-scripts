from sandrock.common import *
from sandrock.lib.asset import Bundle
from sandrock.lib.text import text

import urllib.parse

def find_mission_names() -> dict[int, str | int]:
    bundle = Bundle('story_script')
    mission_names = {}
    script_names = {}
    for asset in bundle.assets:
        if asset.type == 'TextAsset':
            script_id = int(asset.name)
            root = asset.read_xml()
            script_name = urllib.parse.unquote(root.attrib['name'])
            script_names[script_id] = f'{asset.name}:{script_name}'

            name_id = int(root.attrib['nameId'])
            if not name_id:
                continue
            if all(text(name_id, lang) == 'XX' for lang in config.languages):
                continue

            mission_names[script_id] = name_id
            for stmt in root.findall('.//STMT[@stmt="RUN MISSION"]'):
                child_script_id = int(stmt.attrib['missionId'])
                old_name_id = mission_names.get(child_script_id)
                assert not old_name_id or old_name_id == name_id
                mission_names[child_script_id] = name_id

    script_names.update(mission_names)
    return script_names
