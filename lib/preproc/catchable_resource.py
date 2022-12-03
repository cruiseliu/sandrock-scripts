from sandrock.lib.asset import Bundle

def find_catchable_resource_points():
    bundle = Bundle('resourcepoint')
    resources = {}
    for behav in bundle.behaviours:
        if behav.script == 'CatchableResourcePoint':
            resources[behav.game_object.name] = str(behav.path)
    return resources
