from sandrock import *
from sandrock.lib.asset import Bundle
from sandrock.lib.text import *
from sandrock.analyze.item_source.main import get_item_sources
from sandrock.lib.preproc import get_mission_names
from sandrock.lib.unpack import unpack_bundle, unpack_dir

def main():

    unpack_bundle('config')
    unpack_bundle('designer_config')
    unpack_bundle('home')
    unpack_bundle('resourceareainfo')
    unpack_bundle('resourcepoint')
    unpack_bundle('ridable')
    unpack_bundle('story_script')

    for lang in config.languages:
        unpack_bundle(f'localization/{lang}')

    unpack_dir('scene')
    unpack_dir('season')

    unpack_bundle('uisystem_sprite')

main()
